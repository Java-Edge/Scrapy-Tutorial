# 处理获取下载到本地的图片的保存路径

from scrapy.pipelines.images import ImagesPipeline

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        # item传递到pipline后，可以进行很多操作，比如保存到数据库，drop该item，主要做数据存储
        return item

# 到了这一个pipeline，需要做的就是跟数据库或者文件打交道，比如将数据保存到mysql，mangodb，或者本地文件，或者发送到es上面去

# scrapy中的imagepipline只有下载图片的功能，但是我们想将图片在本地保存的地址绑定在一起，并且传到item中
# 定制自己的pipeline，去继承setting中配置的imagespipeline，让里面的某些功能变得可以定制
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 文件最后下载完成的保存路径是存放在results里面的，通过断点调试可以查看这个results是个list，其中每个元素是一个tuple，存放了状态等信息
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item

