# from aiohttp import web
# import re
# import math
# import logging
# import secrets
# import time
# import mimetypes
# from aiohttp.http_exceptions import BadStatusLine
# from dreamxbotz.Bot import multi_clients, work_loads, dreamxbotz
# from dreamxbotz.server.exceptions import FIleNotFound, InvalidHash
# from dreamxbotz.zzint import StartTime, __version__
# from dreamxbotz.util.custom_dl import ByteStreamer
# from dreamxbotz.util.time_format import get_readable_time
# from dreamxbotz.util.render_template import render_page
# from info import *


# routes = web.RouteTableDef()

# @routes.get("/favicon.ico")
# async def favicon_route_handler(request):
#     return web.FileResponse('dreamxbotz/template/favicon.ico')

# @routes.get("/", allow_head=True)
# async def root_route_handler(request):
#     return web.json_response("dreamxbotz")

# @routes.get(r"/watch/{path:\S+}", allow_head=True)
# async def stream_handler(request: web.Request):
#     try:
#         path = request.match_info["path"]
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             id = int(match.group(2))
#         else:
#             id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")
#         return web.Response(text=await render_page(id, secure_hash), content_type='text/html')
#     except InvalidHash as e:
#         raise web.HTTPForbidden(text=e.message)
#     except FIleNotFound as e:
#         raise web.HTTPNotFound(text=e.message)
#     except (AttributeError, BadStatusLine, ConnectionResetError):
#         pass
#     except Exception as e:
#         logging.critical(e.with_traceback(None))
#         raise web.HTTPInternalServerError(text=str(e))

# @routes.get(r"/{path:\S+}", allow_head=True)
# async def stream_handler(request: web.Request):
#     try:
#         path = request.match_info["path"]
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             id = int(match.group(2))
#         else:
#             id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")
#         return await media_streamer(request, id, secure_hash)
#     except InvalidHash as e:
#         raise web.HTTPForbidden(text=e.message)
#     except FIleNotFound as e:
#         raise web.HTTPNotFound(text=e.message)
#     except (AttributeError, BadStatusLine, ConnectionResetError):
#         pass
#     except Exception as e:
#         logging.critical(e.with_traceback(None))
#         raise web.HTTPInternalServerError(text=str(e))

# class_cache = {}

# async def media_streamer(request: web.Request, id: int, secure_hash: str):
#     range_header = request.headers.get("Range", 0)
    
#     index = min(work_loads, key=work_loads.get)
#     faster_client = multi_clients[index]
    
#     if MULTI_CLIENT:
#         logging.info(f"Client {index} is now serving {request.remote}")

#     if faster_client in class_cache:
#         tg_connect = class_cache[faster_client]
#         logging.debug(f"Using cached ByteStreamer object for client {index}")
#     else:
#         logging.debug(f"Creating new ByteStreamer object for client {index}")
#         tg_connect = ByteStreamer(faster_client)
#         class_cache[faster_client] = tg_connect
#     logging.debug("before calling get_file_properties")
#     file_id = await tg_connect.get_file_properties(id)
#     logging.debug("after calling get_file_properties")
    
#     if file_id.unique_id[:6] != secure_hash:
#         logging.debug(f"Invalid hash for message with ID {id}")
#         raise InvalidHash
    
#     file_size = file_id.file_size

#     if range_header:
#         from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
#         from_bytes = int(from_bytes)
#         until_bytes = int(until_bytes) if until_bytes else file_size - 1
#     else:
#         from_bytes = request.http_range.start or 0
#         until_bytes = (request.http_range.stop or file_size) - 1

#     if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
#         return web.Response(
#             status=416,
#             body="416: Range not satisfiable",
#             headers={"Content-Range": f"bytes */{file_size}"},
#         )

#     chunk_size = 1024 * 1024
#     until_bytes = min(until_bytes, file_size - 1)

#     offset = from_bytes - (from_bytes % chunk_size)
#     first_part_cut = from_bytes - offset
#     last_part_cut = until_bytes % chunk_size + 1

#     req_length = until_bytes - from_bytes + 1
#     part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
#     body = tg_connect.yield_file(
#         file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
#     )

#     mime_type = file_id.mime_type
#     file_name = file_id.file_name
#     disposition = "attachment"

#     if mime_type:
#         if not file_name:
#             try:
#                 file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
#             except (IndexError, AttributeError):
#                 file_name = f"{secrets.token_hex(2)}.unknown"
#     else:
#         if file_name:
#             mime_type = mimetypes.guess_type(file_id.file_name)
#         else:
#             mime_type = "application/octet-stream"
#             file_name = f"{secrets.token_hex(2)}.unknown"

#     return web.Response(
#         status=206 if range_header else 200,
#         body=body,
#         headers={
#             "Content-Type": f"{mime_type}",
#             "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
#             "Content-Length": str(req_length),
#             "Content-Disposition": f'{disposition}; filename="{file_name}"',
#             "Accept-Ranges": "bytes",
#         },
#     )
























# # route.py

# from aiohttp import web
# import re
# import math
# import logging
# import secrets
# import time
# import mimetypes
# from aiohttp.http_exceptions import BadStatusLine
# from dreamxbotz.Bot import multi_clients, work_loads, dreamxbotz
# from dreamxbotz.server.exceptions import FIleNotFound, InvalidHash
# from dreamxbotz.zzint import StartTime, __version__
# from dreamxbotz.util.custom_dl import ByteStreamer
# from dreamxbotz.util.time_format import get_readable_time
# from dreamxbotz.util.render_template import render_page
# from info import *

# routes = web.RouteTableDef()

# # --- HELPER FUNCTION FOR FILE SIZE (ADD THIS) ---
# def format_bytes(size):
#     if not size:
#         return ""
#     power = 1024
#     n = 0
#     power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
#     while size > power:
#         size /= power
#         n += 1
#     return f"{round(size, 2)} {power_labels[n]}B"

# @routes.get("/favicon.ico")
# async def favicon_route_handler(request):
#     return web.FileResponse('dreamxbotz/template/favicon.ico')

# @routes.get("/", allow_head=True)
# async def root_route_handler(request):
#     return web.json_response("dreamxbotz")

# # --- (MODIFIED) - WATCH/STREAM PAGE ROUTE ---
# # This route now also generates the link to our new download page
# @routes.get(r"/watch/{path:\S+}", allow_head=True)
# async def stream_handler(request: web.Request):
#     try:
#         path = request.match_info["path"]
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             id = int(match.group(2))
#         else:
#             id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")
            
#         # --- NEW: Generate the URL for the download page ---
#         download_page_url = f"/download/{secure_hash}{id}"
        
#         # You need to modify render_page to accept and use this new URL
#         # For now, let's assume it passes it to the template
#         return web.Response(text=await render_page(id, secure_hash, download_page_url), content_type='text/html')
#     except InvalidHash as e:
#         raise web.HTTPForbidden(text=e.message)
#     except FIleNotFound as e:
#         raise web.HTTPNotFound(text=e.message)
#     except (AttributeError, BadStatusLine, ConnectionResetError):
#         pass
#     except Exception as e:
#         logging.critical(e.with_traceback(None))
#         raise web.HTTPInternalServerError(text=str(e))

# # --- (NEW) - DOWNLOAD PAGE ROUTE ---
# # This route serves the interactive download.html page
# @routes.get(r"/download/{path:\S+}", allow_head=True)
# async def download_page_handler(request: web.Request):
#     try:
#         path = request.match_info["path"]
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if not match:
#             raise FIleNotFound

#         secure_hash, id_str = match.groups()
#         id = int(id_str)
        
#         # Get file properties
#         index = min(work_loads, key=work_loads.get)
#         faster_client = multi_clients[index]
#         tg_connect = ByteStreamer(faster_client)
#         file_id = await tg_connect.get_file_properties(id)
        
#         if file_id.unique_id[:6] != secure_hash:
#             raise InvalidHash

#         file_name = file_id.file_name
#         file_size_bytes = file_id.file_size
#         file_size_formatted = format_bytes(file_size_bytes)
#         file_type = file_name.split('.')[-1].upper() if '.' in file_name else "File"
#         actual_download_url = f"/{secure_hash}{id}"

#         # Read the template file
#         with open("dreamxbotz/template/download.html", "r", encoding="utf-8") as f:
#             template = f.read()

#         # Replace placeholders with actual data
#         page_html = template.replace("{{file_name}}", file_name) \
#                               .replace("{{file_type}}", f"{file_type} Video") \
#                               .replace("{{total_size_formatted}}", file_size_formatted) \
#                               .replace("{{total_size_bytes}}", str(file_size_bytes)) \
#                               .replace("{{actual_download_url}}", actual_download_url)

#         return web.Response(text=page_html, content_type='text/html')
        
#     except InvalidHash:
#         raise web.HTTPForbidden(text="Invalid Link")
#     except FIleNotFound:
#         raise web.HTTPNotFound(text="File Not Found")
#     except Exception as e:
#         logging.error(f"Error in download page handler: {e}", exc_info=True)
#         raise web.HTTPInternalServerError(text="An internal error occurred")


# # --- (UNMODIFIED) - RAW FILE STREAMING ROUTE ---
# # This route remains the same as it serves the actual file bytes.
# @routes.get(r"/{path:\S+}", allow_head=True)
# async def stream_handler(request: web.Request):
#     try:
#         path = request.match_info["path"]
#         match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
#         if match:
#             secure_hash = match.group(1)
#             id = int(match.group(2))
#         else:
#             id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
#             secure_hash = request.rel_url.query.get("hash")
#         return await media_streamer(request, id, secure_hash)
#     except InvalidHash as e:
#         raise web.HTTPForbidden(text=e.message)
#     except FIleNotFound as e:
#         raise web.HTTPNotFound(text=e.message)
#     except (AttributeError, BadStatusLine, ConnectionResetError):
#         pass
#     except Exception as e:
#         logging.critical(e.with_traceback(None))
#         raise web.HTTPInternalServerError(text=str(e))
        
# # ... (media_streamer and other functions remain the same) ...





from aiohttp import web
import re
import math
import logging
import secrets
import mimetypes
import random
from urllib.parse import quote_plus
from aiohttp.http_exceptions import BadStatusLine

from dreamxbotz.Bot import multi_clients, work_loads
from dreamxbotz.server.exceptions import FIleNotFound, InvalidHash
from dreamxbotz.util.custom_dl import ByteStreamer
from dreamxbotz.util.render_template import render_page
from info import *

# --- IMPORTS FOR WEB PAGES ---
from Script import script
# We will import from utils inside functions to prevent circular imports
from database.ia_filterdb import get_search_results
from database.config_db import mdb


routes = web.RouteTableDef()


# --- HTML TEMPLATES (GENERATED DYNAMICALLY) ---

def get_page_template(title, content):
    """Generates a generic HTML page for Help, About, etc."""
    # Local import to break circular dependency
    from utils import temp
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{temp.B_NAME} - {title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .container {{
                background-color: #1e1e1e;
                border-radius: 10px;
                padding: 25px;
                width: 100%;
                max-width: 800px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                border: 1px solid #333;
            }}
            h1 {{
                color: #bb86fc;
                text-align: center;
                border-bottom: 2px solid #bb86fc;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            pre, .content {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 16px;
                line-height: 1.6;
            }}
            a {{
                color: #03dac6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .back-button {{
                display: inline-block;
                margin-top: 25px;
                padding: 10px 20px;
                background-color: #bb86fc;
                color: #121212;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
                transition: background-color 0.3s;
            }}
            .back-button:hover {{
                background-color: #a062f6;
                text-decoration: none;
            }}
            .search-list {{
                list-style-type: none;
                padding: 0;
            }}
            .search-list li {{
                background-color: #2a2a2a;
                padding: 10px;
                margin-bottom: 8px;
                border-radius: 5px;
                border-left: 3px solid #03dac6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <div class="content">{content}</div>
        </div>
        <a href="/" class="back-button">« Back to Home</a>
    </body>
    </html>
    """

# --- ROUTES DEFINITION ---

@routes.get("/favicon.ico")
async def favicon_route_handler(request):
    return web.FileResponse('dreamxbotz/template/favicon.ico')

@routes.get("/", allow_head=True)
async def root_route_handler(request: web.Request):
    """
    Serves the main start page with an integrated search bar and results display.
    """
    # Local imports to break circular dependency
    from utils import temp, get_size

    query = request.rel_url.query.get("query", "").strip()
    search_results_html = ""

    # If a search query is provided in the URL, perform the search
    if query:
        files, offset, total_results = await get_search_results(chat_id=None, query=query.lower(), offset=0, filter=True)
        
        if files:
            search_results_html += f"<div class='results-header'>Found {total_results} results for '<b>{query}</b>'</div>"
            search_results_html += '<ul class="results-list">'
            for file in files:
                file_hash = file.unique_id[:6]
                file_id = file.file_id
                
                watch_url = f"/watch/{file_hash}{file_id}"
                download_url = f"/{file_hash}{file_id}"
                file_size_formatted = get_size(file.file_size) # Use get_size from utils

                search_results_html += f"""
                <li>
                    <div class="file-info">
                        <span class="file-name">{file.file_name}</span>
                        <span class="file-size">{file_size_formatted}</span>
                    </div>
                    <div class="file-actions">
                        <a href="{watch_url}" target="_blank" class="action-btn watch">Watch Online</a>
                        <a href="{download_url}" class="action-btn download">Download</a>
                    </div>
                </li>
                """
            search_results_html += "</ul>"
        else:
            search_results_html = f"<div class='results-header'>No results found for '<b>{query}</b>'</div>"

    # HTML structure for the entire page
    bot_name = temp.B_NAME
    background_image = random.choice(PICS)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search - {bot_name}</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                font-family: 'Roboto', sans-serif;
                color: white;
                background-color: #121212;
            }}
            .bg-container {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }}
            .bg {{
                background-image: url('{background_image}');
                height: 100%;
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                filter: blur(5px) brightness(0.4);
                transform: scale(1.1);
            }}
            .content-wrapper {{
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 2.8em;
                margin-bottom: 10px;
                color: #fff;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
            }}
            .search-container {{
                background: rgba(30, 30, 30, 0.8);
                padding: 25px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }}
            .search-form {{
                display: flex;
                gap: 10px;
            }}
            .search-input {{
                flex-grow: 1;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #444;
                background-color: #2a2a2a;
                color: white;
                font-size: 1em;
            }}
            .search-button {{
                padding: 15px 25px;
                border: none;
                border-radius: 8px;
                background-color: #bb86fc;
                color: #121212;
                font-size: 1em;
                font-weight: bold;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .search-button:hover {{ background-color: #a062f6; }}
            .search-results {{ margin-top: 30px; }}
            .results-header {{
                font-size: 1.2em;
                color: #e0e0e0;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #444;
            }}
            .results-list {{ list-style: none; padding: 0; }}
            .results-list li {{
                background-color: rgba(42, 42, 42, 0.8);
                border-radius: 8px;
                margin-bottom: 10px;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
                transition: background-color 0.2s;
            }}
            .results-list li:hover {{ background-color: rgba(60, 60, 60, 0.8); }}
            .file-info {{ flex-grow: 1; }}
            .file-name {{ display: block; font-size: 1.1em; margin-bottom: 5px; }}
            .file-size {{ font-size: 0.9em; color: #aaa; }}
            .file-actions {{ display: flex; gap: 10px; }}
            .action-btn {{
                padding: 8px 15px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: background-color 0.3s, transform 0.2s;
            }}
            .action-btn.watch {{ background-color: #03dac6; color: #121212; }}
            .action-btn.download {{ background-color: #cf6679; color: white; }}
            .action-btn:hover {{ transform: translateY(-2px); }}
        </style>
    </head>
    <body>
        <div class="bg-container"><div class="bg"></div></div>
        <div class="content-wrapper">
            <div class="header">
                <h1>{bot_name}</h1>
            </div>
            <div class="search-container">
                <form action="/" method="GET" class="search-form">
                    <input type="text" name="query" class="search-input" placeholder="Search for movies or series..." value="{query}" required>
                    <input type="submit" class="search-button" value="Search">
                </form>
            </div>
            <div class="search-results">
                {search_results_html}
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/help", allow_head=True)
async def help_page_handler(request):
    """Serves the help page."""
    help_content = f"<pre>{script.HELP_TXT}</pre>"
    html_content = get_page_template("Help", help_content)
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/about", allow_head=True)
async def about_page_handler(request):
    """Serves the about page."""
    # Local import to break circular dependency
    from utils import temp
    about_content = script.ABOUT_TXT.format(
        U_NAME=temp.U_NAME,
        B_NAME=temp.B_NAME,
        OWNER_LNK=OWNER_LNK
    )
    about_content = f"<div>{about_content}</div>"
    html_content = get_page_template("About", about_content)
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/upgrade", allow_head=True)
async def upgrade_page_handler(request):
    """Serves the upgrade/premium page."""
    upgrade_content = f"<pre>{script.PREPLANS_TXT.format(mention='User', upi=OWNER_UPI_ID, qr=QR_CODE)}</pre>"
    html_content = get_page_template("Upgrade to Premium", upgrade_content)
    return web.Response(text=html_content, content_type='text/html')

@routes.get("/topsearches", allow_head=True)
async def top_searches_handler(request):
    """Serves a page with the top searches."""
    limit = 20
    top_messages = await mdb.get_top_messages(limit)
    
    seen_messages = set()
    clean_messages = []
    for msg in top_messages:
        msg_lower = msg.lower()
        if msg_lower not in seen_messages and bool(re.match('^[a-zA-Z0-9 ]*$', msg)):
            seen_messages.add(msg_lower)
            clean_messages.append(msg)
            
    if clean_messages:
        search_list_html = '<ul class="search-list">'
        for item in clean_messages:
            search_list_html += f'<li>{item}</li>'
        search_list_html += '</ul>'
    else:
        search_list_html = '<p>No top searches available right now.</p>'
    
    html_content = get_page_template("Top Searches of the Day", search_list_html)
    return web.Response(text=html_content, content_type='text/html')

@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def watch_page_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
            
        download_page_url = f"/download/{secure_hash}{id}"
        return web.Response(text=await render_page(id, secure_hash, download_page_url), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

@routes.get(r"/download/{path:\S+}", allow_head=True)
async def download_page_handler(request: web.Request):
    # Local import to break circular dependency
    from utils import get_size
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if not match:
            raise FIleNotFound

        secure_hash, id_str = match.groups()
        id = int(id_str)
        
        index = min(work_loads, key=work_loads.get)
        faster_client = multi_clients[index]
        tg_connect = ByteStreamer(faster_client)
        file_id = await tg_connect.get_file_properties(id)
        
        if file_id.unique_id[:6] != secure_hash:
            raise InvalidHash

        file_name = file_id.file_name
        file_size_bytes = file_id.file_size
        file_size_formatted = get_size(file_size_bytes)
        file_type = file_name.split('.')[-1].upper() if '.' in file_name else "File"
        actual_download_url = f"/{secure_hash}{id}"

        with open("dreamxbotz/template/download.html", "r", encoding="utf-8") as f:
            template = f.read()

        page_html = template.replace("{{file_name}}", file_name) \
                              .replace("{{file_type}}", f"{file_type} Video") \
                              .replace("{{total_size_formatted}}", file_size_formatted) \
                              .replace("{{total_size_bytes}}", str(file_size_bytes)) \
                              .replace("{{actual_download_url}}", actual_download_url)

        return web.Response(text=page_html, content_type='text/html')
        
    except InvalidHash:
        raise web.HTTPForbidden(text="Invalid Link")
    except FIleNotFound:
        raise web.HTTPNotFound(text="File Not Found")
    except Exception as e:
        logging.error(f"Error in download page handler: {e}", exc_info=True)
        raise web.HTTPInternalServerError(text="An internal error occurred")

@routes.get(r"/{path:\S+}", allow_head=True)
async def raw_file_stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))
        
class_cache = {}

async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
    else:
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
        
    file_id = await tg_connect.get_file_properties(id)
    
    if file_id.unique_id[:6] != secure_hash:
        raise InvalidHash
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type, _ = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": mime_type or "application/octet-stream",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{quote_plus(file_name)}"',
            "Accept-Ranges": "bytes",
        },
    )
