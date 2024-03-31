from nicegui import ui,events
from pathlib import Path
import pypandoc
from unoserver.client import UnoClient
from dotenv import dotenv_values
import convertapi


class fileflip_utils:
  def __init__(self):
    ui.page_title("FileFlip")
    self.client = UnoClient()
    self.config = dotenv_values(f"{Path.cwd()}/config.env")
    self.input_file_name = None
    self.output_file_format = None
    self.pandoc_supported_formats = pypandoc.get_pandoc_formats()[1]
    self.unoserver_supported_formats = ['odt','csv','doc','docx','dotx','fodp','fods','fodt','mml','odb','odf','odg','odm','odp','ods','otg','otp','ots','xls','xlsx','pptx','pdf']
    self.all_supported_formats = sorted(set(self.pandoc_supported_formats + self.unoserver_supported_formats))
    convertapi.api_secret = self.config['API_SECRET']

  def on_upload(self,e:events.UploadEventArguments):
    file_data = e.content.read()
    self.input_file_name = e.name
    with open(f"{Path.cwd()}/temp_files/input/{self.input_file_name}","wb") as file:
      file.write(file_data)
  

  def convert_file(self):
    input_file_format = Path(f"{Path.cwd()}/temp_files/input/{self.input_file_name}").suffix.split('.')[1]
    if input_file_format and self.output_file_format in self.all_supported_formats:
      try:
        ui.notify('Your file is converting ...', close_button='OK')
        pypandoc.convert_file(source_file=f"{Path.cwd()}/temp_files/input/{self.input_file_name}",to=self.output_file_format,outputfile=f"{Path.cwd()}/temp_files/output/{self.input_file_name.split('.')[0]}.{self.output_file_format}")
      except:
          self.client.convert(inpath=f"{Path.cwd()}/temp_files/input/{self.input_file_name}",outpath=f"{Path.cwd()}//temp_files/output/{self.input_file_name.split('.')[0]}.{self.output_file_format}",convert_to=self.output_file_format)
          '''
          result = convertapi.convert(self.output_file_format, { 'File': f"{Path.cwd()}/temp_files/input/{self.input_file_name}" })
          if result:
            result.file.save(f"{Path.cwd()}//temp_files/output/{self.input_file_name.split('.')[0]}.{self.output_file_format}")
          else:
            ui.notify("Conversion failed")
            '''
      else:
        ui.notify("Conversion successful",type="positive")
        ui.navigate.to("/download")
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
      ui.select(self.all_supported_formats,value='select',on_change=lambda e: setattr(self,'output_file_format',e.value)).classes('convert-dropdown')
      ui.button('convert',color='purple',on_click=lambda: self.convert_file()).classes('convert-button')
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
      ui.upload(max_files=1,on_upload=lambda e : self.on_upload(e)).classes('upload-section')
      ui.button('upload',color='purple',on_click=lambda: ui.navigate.to("/convert")).classes('upload-button')
    return upload_ui_card
  
  def render_download_ui(self):
    # temporary section
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{
        background-color: #161616;
      }
      .download-label-1{
        position: relative;
        font-size: 2.5em;
        color: white;
        font-family: arial;
        left: 35vw;
        top: 7vw;
      }
      .download-label-2{
        position: relative;
        font-size: 1.2em;
        left: 5.5vw;
        top: 2vh;
      }
      .download-label-3{
        position: relative;
        font-size: 1.2em;
        left: 5.5vw;
        top: 1vh;
      }
      .download-card {
        background-color: #333;
        color: white;
        width: 30vw;
        height: 20vw;         
        box-shadow: 0 0 20px 10px #b400ff;
        left: 35vw;
        top: 21vh;
      }
      .download-button{
        position: relative;
        top: 10vh;
        left: 10vw;
      }
      </style>''')
    ui.label('download your files here ⬇️').classes('download-label-1')
    with ui.card().classes('download-card') as download_ui_card:
      ui.label("Your file has been converted").classes("download-label-3")
      ui.label(f"From {self.input_file_name} to {self.output_file_format}").classes("download-label-2")
      ui.button('upload',color='purple',on_click= lambda: ui.download(src=f"{Path.cwd()}/temp_files/output/{self.input_file_name.split('.')[0]}.{self.output_file_format}")).classes('upload-button')
    return download_ui_card