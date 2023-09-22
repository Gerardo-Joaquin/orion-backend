import time
from boto3.session import Session
import json
import requests
import os

class TranscribeWrapper:
	"""Class to wrap processes to get transcription for an audio."""
    
	def __init__(self, aws_credentials, bucket="bucket-vplusplus"):
		"""Create a wrapper for transcribe.

		:param aws_credentials: dict: dict with credentials
		:param bucket: str: bucket of S3
		"""
		self.session = Session(
			aws_access_key_id=aws_credentials["aws_access_key_id"],
			aws_secret_access_key=aws_credentials["aws_secret_access_key"],
			aws_session_token=aws_credentials["aws_session_token"],
		)
		self.transcribe_client = self.session.client("transcribe", region_name="us-east-1")
		self.s3_client = self.session.client("s3")
		self.bucket = bucket

	def store_file_s3(self, file_path, s3_path):
		"""
		Upload file to S3.

		:param file_path: str: path for file to upload (absolute)
		:param s3_path: str: path for final location

		Returns
			URI for uploaded file
		"""

		# path local, bucket, path bucket
		self.s3_client.upload_file(file_path, self.bucket, s3_path)

		url = "s3://%s/%s" % (self.bucket, s3_path)

		# Remove comment for production
		#os.remove(file_path)

		return url
	
	def download_file_s3(self, file_uri):
		"""
		Download stored file from S3

		:param file_uri: str: Path for file to download in S3

		Return
			Extracted text from file in S3
		"""
		response = requests.get(file_uri)

		json_response = json.loads(response.content)
		text = " ".join(
				[
					transcript["transcript"] 
					for transcript in json_response["results"]["transcripts"]
				]
			)

		return text

	def transcribe_file(self, job_name, file_uri, media_format="mp3"):
		"""Transcribe a file stored in S3. 
		
		:param job_name: str: name for transcribe job
		:param file_uri: str: uri S3 for audio file
		:param media_format: str: default mp3
		
		Return
			Text generated from transcribe
		"""
		self.transcribe_client.start_transcription_job(
			TranscriptionJobName=job_name,
			Media={'MediaFileUri': file_uri},
			MediaFormat=media_format,
			LanguageCode='es-ES'
		)

		max_tries = 60
		while max_tries > 0:
			max_tries -= 1
			job = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
			job_status = job['TranscriptionJob']['TranscriptionJobStatus']
			if job_status in ['COMPLETED', 'FAILED']:
				print(f"Job {job_name} is {job_status}.")
				break
			else:
				print(f"Waiting for {job_name}. Current status is {job_status}.")
			time.sleep(10)

		return job['TranscriptionJob']['Transcript']['TranscriptFileUri']
	
	def delete_transcribe_job(self, transcribe_job):
		"""Delete a transcription job.
		
		:param transcribe_job: str: transcription job
		"""
		response = self.transcribe_client.delete_transcription_job(
			TranscriptionJobName=transcribe_job
		)
		print(response)

	def operate_transcription(self, file_path, media_format="mp3"):
		"""Orchestator of functions to get a transcription.
		
		:param file_path: path for audio file
		:param media_format: str: mp3 default

		returns
			Transcribed phrase
		"""
		job_name = "transcription"
		file_uri = self.store_file_s3(file_path=file_path, s3_path="audios/audio.mp3")

		transcription_uri = self.transcribe_file(
			job_name=job_name, 
			file_uri=file_uri, 
			media_format=media_format
		)

		phrase = self.download_file_s3(transcription_uri)
		self.delete_transcribe_job(job_name)

		print(f"Phrase: {phrase}")

		return phrase


def main():
	# Dejo setteadas las credenciales para temas de testing, no hacer publicas!
	credentials = {
		"aws_access_key_id": "",
		"aws_secret_access_key": "",
		"aws_session_token": ""
	}
	object_transcribe = TranscribeWrapper(credentials)
	object_transcribe.operate_transcription(file_path="/Users/abraham.lazaro/Downloads/hola.mp3")

if __name__ == '__main__':
    main()
