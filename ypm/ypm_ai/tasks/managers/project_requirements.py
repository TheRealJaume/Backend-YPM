import os
import requests

import assemblyai as aai
from django.conf import settings
from django.core.files.storage import default_storage
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from ypm_ai.tasks.prompts.project.models import ProjectRequirements, RequirementsFromText
from ypm_ai.tasks.prompts.project.text import summarize_requirements_prompt, get_requirements_from_text_prompt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class RequirementsManager:

    def __init__(self, audio_file=None, requirements_text=None, text_file=None):
        load_dotenv()
        self.audio_file = audio_file
        self.text_file = text_file
        self.requirements_text = requirements_text
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.text_model = genai.GenerativeModel("gemini-1.5-flash")

    def transcript_audio(self, file_url, text_with_speaker_labels=''):
        try:
            # Use model to transcript audio from text
            config = aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.best,
                speaker_labels=True,
                language_code="es"
            )
            # Download file from S3 if exists
            transcriber = aai.Transcriber(config=config)
            logger.info("DJANGO ENV", os.getenv("DJANGO_ENV"))
            if os.getenv('DJANGO_ENV') == 'production':
                local_file_path = '/media/local_copy.pdf'
                self.download_file_from_url(self.text_file, local_file_path)
                transcript = transcriber.transcribe(local_file_path)
            else:
                transcript = transcriber.transcribe(f"./media/{file_url}")

            if transcript.status == aai.TranscriptStatus.error:
                logger.error("Error en la transcripción: ", transcript.error)
                raise Exception(transcript.error)
            else:
                # Iterate through the transcript to label the conversations
                for utt in transcript.utterances:
                    text_with_speaker_labels += f" Speaker {utt.speaker}:\n{utt.text}\n"
                return text_with_speaker_labels
        except Exception as e:
            logger.error("Error en la transcripción: ", e)
            return str(e)

    def get_requirements_from_conversation(self):
        # Request the number of tasks per department and per phase
        requirements_prompt = summarize_requirements_prompt(self.requirements_text)

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=ProjectRequirements)

        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        requirements_chain = (
                prompt
                | self.model
                | parser)

        result = requirements_chain.invoke({
            "query": requirements_prompt
        })
        return result

    def get_requirements_from_text(self):
        try:
            local_file_path = '/media/local_copy.pdf'
            self.download_file_from_url(self.text_file, local_file_path)
            # Subir el archivo al servicio externo
            doc_file = genai.upload_file(local_file_path)
            # Get the requirements prompt from text file
            prompt = get_requirements_from_text_prompt()
            # Get the output structure for the requirements
            result = self.text_model.generate_content([doc_file, "\n\n", prompt],
                                                      generation_config=genai.GenerationConfig(
                                                          response_mime_type="application/json",
                                                          response_schema=RequirementsFromText
                                                      ),
                                                      )
        except Exception as e:
            logging.error("Failed to generate requirements: %s", str(e))
        return result.text


    def download_file_from_url(self, url, local_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception(f"Failed to download file. Status code: {response.status_code}")
