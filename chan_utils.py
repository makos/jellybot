import re
from BeautifulSoup import BeautifulSoup

def get_id(node):

  id = int(node['id'])
  
  return id

def get_name(node):
  name_nodes = node.findAll('span', {"class": "commentpostername"})        
  
  if len(name_nodes) > 0:
    name_node = name_nodes[0]
    name = strip_html(name_nodes[0].renderContents())
  else:
    name = None
  
  return name

def get_email(node):
  email = None
  email_nodes = node.findAll("a", { "class" : "linkmail" } )
  
  if len(email_nodes) > 0:
    email = email_nodes[0]['href'][7:]
    return email

def get_date(node, is_reply, post_id):
  if is_reply:
    number_node = node.find(id = 'norep' + str(post_id))
  else:
    number_node = node.find(id = 'nothread' + str(post_id))
    date_string = number_node.previousSibling.strip()
  
  try:
    date = datetime.strptime(date_string, "%m/%d/%y(%a)%H:%M:%S")
  except:
    date = None
  
  return date

def get_trip_code(node):
  
  trip_nodes = node.findAll("span", { "class": "postertrip" })
  
  if len(trip_nodes) > 0:
    trip_code = trip_nodes[0].renderContents()
  else:
    trip_code = None
  
  return trip_code

def get_text(node):
  text_nodes = node.findAll("blockquote")
  text = None
  if len(text_nodes) > 0 and len(text_nodes[0].contents) > 0:
    text = strip_html(text_nodes[0].renderContents())
    return text

def get_img_data(node):
  img_nodes = node.findAll("span", { "class" : "filesize" })
  
  img_url = None
  img_url_filename = None
  img_source_filename = None
  img_kb = None
  img_width = None
  img_height = None
  
  if len(img_nodes) > 0:
    img_url = img_nodes[0].a['href']
    img_url_filename = img_nodes[0].a.renderContents()
    img_source_filename = img_nodes[0].find('span')['title']
       
    file_info = img_nodes[0].a.nextSibling.strip()
    
    hit_re = re.match("-\((?P<filesize>\d+\.?\d*) (?P<units>(B|KB|MB)), (?P<width>\d+)x(?P<height>\d+),", file_info)
    
    if hit_re:
      img_kb = float(hit_re.group("filesize"))
      
      if hit_re.group("units") == "B":
        img_kb /= 1024 # bytes in a KB
      elif hit_re.group("units") == "MB":
        img_kb *= 1024  # KB in a MB
        img_width = int(hit_re.group("width"))
        img_height = int(hit_re.group("height"))
    
    return [img_url, img_url_filename, img_source_filename, img_kb, img_width, img_height]

def get_subject(node):

    subject = None
    subject_nodes = node.findAll('span', { "class": "replytitle" } )

    if len(subject_nodes) > 0 and subject_nodes[0].renderContents() != "":
        subject = subject_nodes[0].renderContents()

    return subject

def strip_html(contents):
  return ' '.join(BeautifulSoup(contents).findAll(text=True))
