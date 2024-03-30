from nicegui import ui
from pathlib import Path
import pypandoc
from unoserver.client import UnoClient
import psutil
from dotenv import dotenv_values
import os
import convertapi


class fileflip_utils:
  def __init__(self):
    self.client = UnoClient()
    self.config = dotenv_values(f"{Path.cwd()}/config.env")
    self.input_file_name = None
    self.pandoc_supported_formats = pypandoc.get_pandoc_formats()[1]
    self.unoserver_supported_formats = ['.odt','.csv','.doc','.docx','.dotx','.fodp','.fods','.fodt','.mml','.odb','.odf','.odg','.odm','.odp','.ods','.otg','.otp','.ots']
    self.all_supported_formats = sorted(set(self.pandoc_supported_formats + self.unoserver_supported_formats))
    convertapi.api_secret = self.config['API_SECRET']
    
  def convert_file(self,input_file_name,output_file_format):
    self.input_file_format = Path.suffix(f"{Path.cwd()}/temp_files/input/{input_file_name}")
    if self.input_file_format in self.all_supported_formats and output_file_format in self.all_supported_formats:
      try:
        ui.notify('Your file is converting ...', close_button='OK')
        pypandoc.convert_file(f"{Path.cwd()}/temp_files/input/{input_file_name}",format=output_file_format,outputfile=f"{Path.cwd()}/temp_files/output/{input_file_name.split('.')[0]}.{output_file_format}")
      except:
        try:
          self.client.convert(inpath=f"{Path.cwd()}/temp_files/input/{input_file_name}",outpath=f"{Path.cwd()}//temp_files/output/{input_file_name.split('.')[0]}.{output_file_format}",convert_to=output_file_format)
        except:
          result = convertapi.convert(output_file_format, { 'File': f"{Path.cwd()}/temp_files/input/{input_file_name}" })
          if result:
            result.file.save(f"{Path.cwd()}//temp_files/output/{input_file_name.split('.')[0]}.{output_file_format}")
          else:
            ui.notify("Conversion failed")
      else:
        ui.notify("Conversion successful",type="positive")
    else:
       ui.notify('This format is not supported', type='negative')
    
  def render_conversion_ui(self):
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{
        background-color: #161616;
      }
      .convert-label-1{
        position: relative;
        font-size: 2.5em;
        color: white;
        font-family: arial;
        left: 37vw;
        top: 7vw;
      }
      .convert-label-2{
        position: relative;
        font-size: 1.2em;
        left: 5.5vw;
        top: 2vh;
      }
      .convert-card {
        background-color: #333;
        color: white;
        width: 30vw;
        height: 20vw;         
        box-shadow: 0 0 20px 10px #b400ff;
        left: 35vw;
        top: 21vh;
      }
      .convert-dropdown {
        position: relative;
        width: 10vw;
        height: 10vh;
        top: 6vh;
        background-color: grey;
        border: 1px solid #ccc;
        border-radius: 4px;
        left: 8.5vw;
      }
      .convert-button{
        position: relative;
        top: 12vh;
        left: 10vw;
      }
      </style>''')
    ui.label('Flip your files here 😉').classes('convert-label-1')
    with ui.card().classes('convert-card') as convert_ui_card:
      ui.label('Select your output format 👇').classes('convert-label-2')
      output_format = ui.select(self.all_supported_formats,value='select').classes('convert-dropdown')
      ui.button('convert',color='purple').classes('convert-button')
    return convert_ui_card
  
  def render_upload_ui(self):
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{
        background-color: #161616;
      }
      .upload-label{
        position: relative;
        font-size: 2.5em;
        color: white;
        font-family: arial;
        left: 35vw;
        top: 7vw;
      }
      .upload-card {
        background-color: #333;
        color: white;
        width: 30vw;
        height: 20vw;         
        box-shadow: 0 0 20px 10px #b400ff;
        left: 35vw;
        top: 21vh;
      }
      .upload-button{
        position: relative;
        top: 10vh;
        left: 10vw;
      }
      .upload-section{
       postion: relative;
        top: 5vh;
        left: 1.2vw;
        background-color: #808080;
      }
      </style>''')
    ui.label('Upload your files here ⬆️').classes('upload-label')
    with ui.card().classes('upload-card') as upload_ui_card:
      ui.upload(max_files=1).classes('upload-section')
      ui.button('upload',color='purple').classes('upload-button')
    return upload_ui_card
  
  def render_download_ui():
    ui.label("Download page")
      