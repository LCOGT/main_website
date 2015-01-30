'''
Utility functions for importing content from Drupal
'''

import re, json, HTMLParser
import MySQLdb
from settings import DATABASES as dbc
from mezzanine.generic.models import Keyword, AssignedKeyword
from django.conf import settings

def get_media(dbname):
    media_dict = {}
    db = MySQLdb.connect(user=dbc['drupal']['USER'], passwd=dbc['drupal']['PASSWORD'], db=dbname, host=dbc['rbauth']['HOST'])

    # Match supplied user name to one in Drupal database
    sql_users = "SELECT fid, uri FROM file_managed"
    media_link = db.cursor()
    media_link.execute(sql_users)
    media_files = media_link.fetchall()
    media_link.close()
    db.close()
    for mf in media_files:
        if mf[1][0:9] == 'public://':
            media_dict[str(mf[0])] = mf[1][9:]
    return media_dict


def links_to_text(page_list, activities):
    html = "<ul>"
    for item in page_list:
        activity = activities[item]
        html += "<li><a href='%s'>%s</li>" % ()
    html += "</ul>"
    return html

def find_media_tag(content):
    lines = []
    medias = re.findall('(\[+\{"type":"media".*\n?\}\]+)', content, re.MULTILINE)
    if medias:
        for media in medias:
            try:                  
                line = json.loads(media)
                new_media = {'orig':media,'values':line[0][0]}
                lines.append(new_media)
            except:
                pass
    return lines

def make_img_tag(media,line):
    fid = line['fid']
    filename = media.get(fid,None)
    tag = "<img src='%s%s' title='%s' style='%s' height='%s' width='%s' class='%s' />"
    if filename:
        title = line['attributes'].get('title','')
        style = line['attributes'].get('style','')
        height = line['attributes'].get('height','')
        width = line['attributes'].get('width','')
        css_class = line['attributes'].get('css_class','')
        html = HTMLParser.HTMLParser()
        imgtag = tag % (settings.MEDIA_URL,filename, title, style, height, width, css_class)
        return html.unescape(imgtag)
    else:
        return None

def replace_media_tag(content,media):
    lines = find_media_tag(content)
    for line in lines:
        tag = make_img_tag(media,line['values'])
        if tag:
            content = content.replace(line['orig'],tag)
    return content




def set_keywords(page, disciplines, spacebook=False):
    categories = {'6':'education','8':'science','5143':'observatory','9':'observatory','7':'observatory'}
    for disc in disciplines:
        try:
            kw = categories[disc['nid']]
            keyword_id = Keyword.objects.get_or_create(title=kw)[0].id
            page.keywords.add(AssignedKeyword(keyword_id=keyword_id))
        except Exception, e:
            print e
    if spacebook:
        keyword_id = Keyword.objects.get_or_create(title='spacebook')[0].id
        page.keywords.add(AssignedKeyword(keyword_id=keyword_id))
    return True