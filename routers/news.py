#模块化路由
from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news,news_cache

#创建APIRouter实例
#prefix为前缀，tags为标签
router=APIRouter(prefix="/api/news",tags=["news"])

#定义新闻分类路由
@router.get("/categories")
async def categories(skip: int = 0, limit: int = 100, db:AsyncSession=Depends(get_db)):
    #获取数据库中的新闻分类
    print("接口被调用了！", skip, limit)
    categories = await news_cache.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize",le=100),
        db:AsyncSession=Depends(get_db)
):
    offset = (page-1) * page_size
    news_list = await news_cache.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    #(跳过的+当前列表数量)<总数
    has_more = (offset+len(news_list))<total
    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }
@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news_cache.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_news = await news_cache.get_related_news(db, news_detail.id, news_detail.category_id)

    return {
      "code": 200,
      "message": "success",
      "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
      }
    }
