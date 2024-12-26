"""
# 북마크 페이지 > 리스트 조회
@app.post("/api/bookmark/list")
async def select_bookmark_info(ContentsList :RequestBookmarkSchema):
    from bookmark.modules.bookmark import select_bookmarks
    if ContentsList:
        return select_bookmarks(ContentsList.idtype, ContentsList.idcode, ContentsList.mapx, ContentsList.mapy)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
# 핫플 게시글 > 북마크 하기
@app.post("/api/bookmark/creation")
async def create_bookmark_info(BookmarkCreation :RequestBookmarkSchema):
    from bookmark.modules.bookmark import insert_bookmarks
    if BookmarkCreation:
        return insert_bookmarks(BookmarkCreation.idtype, BookmarkCreation.idcode, BookmarkCreation.contentid, BookmarkCreation.bookmark_nickname)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
# 북마크 페이지 > 북마크 제거, 핫플 게시글 > 북마크 제거
@app.post("/api/bookmark/delete")
async def delete_bookmarks_info(BookmarkDelete:RequestBookmarkSchema):
    from bookmark.modules.bookmark import delete_bookmarks
    if BookmarkDelete:
        return delete_bookmarks(BookmarkDelete.idtype, BookmarkDelete.idcode, BookmarkDelete.contentid)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
# 북마크 여부 > 핫플 게시글
@app.post("/api/bookmark/check")
async def check_bookmarks_info(BookmarkCheck: RequestBookmarkSchema):
    from bookmark.modules.bookmark import check_bookmarks
    if BookmarkCheck:
        return check_bookmarks(BookmarkCheck.idtype, BookmarkCheck.idcode, BookmarkCheck.contentid)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
# 북마크 수정
@app.post("/api/bookmark/update")
async def update_bookmarks_info(BookmarkUpdate:RequestBookmarkSchema):
    from bookmark.modules.bookmark import update_bookmarks
    if BookmarkUpdate:
        return update_bookmarks(BookmarkUpdate.idtype, BookmarkUpdate.idcode, BookmarkUpdate.contentid, BookmarkUpdate.bookmark_nickname)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
"""