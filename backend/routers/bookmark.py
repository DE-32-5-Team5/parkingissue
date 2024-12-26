"""
from fastapi import APIRouter
from models.bookmark import (
   BookmarkListSchema,
   BookmarkCreationSchema,
   BookmarkCheckSchema,
   BookmarkDeleteSchema,
   BookmarkUpdateSchema,
)
from services.bookmark import (
    select_bookmark_info,
    create_bookmark_info,
    delete_bookmarks_info,
    check_bookmarks_info,
    update_bookmarks_info,
)

 r_bookmark = APIRouter(
    prefix = "/api/bookmark",
    tags = ["bookmark"],
)

@r_bookmark.post('/list')
async def bookmark_list():
    return await select_bookmark_info()
"""