# SDK for Python


The SDK for Python contains two parts:
1. CLI Tool
2. Utility Tools

## CLI Tool

The CLI Tool is mainly designed for those who are more comfortable using command line tools.

The installation of the CLI Tool is:pip install elcrawlsdk

Then, you can use the `elcrawl` command in the command prompt.  elcrawl --help


## Utility Tools

Utility tools mainly provide some `helper` methods to make it easier for you to integrate your spiders into platform, e.g. saving results.


##### Scrapy Integration

In `settings.py` in your Scrapy project, find the variable named `ITEM_PIPELINES` (a `dict` variable). Add content below.

```python
ITEM_PIPELINES = {
    'elcrawl.pipelines.ElcrawlMongoPipeline': 888,
}
```

Then, start the Scrapy spider. After it's done, you should be able to see scraped results in **Task Detail -> Result**

##### General Python Spider Integration

Please add below content to your spider files to save results.

```python
# import result saving method
from elcrawl import save_item

# this is a result record, must be dict type
result = {'name': 'elcrawl'}

# call result saving method
save_item(result)
```
Then, start the spider. After it's done, you should be able to see scraped results in **Task Detail -> Result**
