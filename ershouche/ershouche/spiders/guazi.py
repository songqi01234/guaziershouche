# -*- coding: utf-8 -*-
import scrapy
import time


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    start_urls = ['https://www.guazi.com/www/buy/']
    cookies = {'uuid':'478dcee0-9b59-4c6d-f05f-c3246d3d8149',' ganji_uuid':'2436157119854553358394',' __utmganji_v20110909':'db176341-4252-4ba1-be14-890d4b4b5498',' close_finance_popup':'2017-12-16',' antipas':'K7Z6553v031576486L8A5i1h4X1',' cityDomain':'www',' clueSourceCode':'%2A%2300',' cainfo':'%7B%22ca_s%22%3A%22sem_baiduss%22%2C%22ca_n%22%3A%22bdpc_sye%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22%25E7%2593%259C%25E5%25AD%2590%25E7%2593%259C%25E5%25AD%2590%25E4%25BA%258C%25E6%2589%258B%25E8%25BD%25A6%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e4%25ba%258c%25e6%2589%258b%25e8%25bd%25a6%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%2265097766814%22%2C%22scode%22%3A%2210103188612%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22478dcee0-9b59-4c6d-f05f-c3246d3d8149%22%2C%22sessionid%22%3A%221e9006d8-f8bb-4308-b5bd-755c9b8c0a34%22%7D',' preTime':'%7B%22last%22%3A1513435463%2C%22this%22%3A1510487149%2C%22pre%22%3A1510487149%7D',' lg':'1',' Hm_lvt_e6e64ec34653ff98b12aab73ad895002':'1512921190,1513392371,1513407919,1513435459',' Hm_lpvt_e6e64ec34653ff98b12aab73ad895002':'1513435462',' sessionid':'1e9006d8-f8bb-4308-b5bd-755c9b8c0a34'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies=self.cookies,
                callback=self.parse,
            )

    def parse(self, response):
        time.sleep(0.7)
        li_list = response.xpath('//ul[@class="carlist clearfix js-top"]/li')
        for li in li_list:
            item = {}
            item['车辆名称'] = li.xpath('.//h2[@class="t"]/text()').extract_first()
            item['车辆价格'] = li.xpath('.//div[@class="t-price"]/p/text()').extract_first()
            item['车辆价格'] = item['车辆价格'] + '万'
            item['url地址'] = li.xpath('./a/@href').extract_first()
            if item['url地址'] is not None:
                item['url地址'] = 'https://www.guazi.com' + item['url地址']
            # print(item)
            # 获取详情页
            cat_url_temp = li.xpath('./a/@href').extract_first()
            if cat_url_temp is not None:
                cat_url = 'https://www.guazi.com' + cat_url_temp
                # print(cat_url)
                yield scrapy.Request(
                    cat_url,
                    cookies=self.cookies,
                    meta={'item': item},
                    callback=self.parse_car
                )
        # 获取下一页
        next_url_temp = response.xpath('//a[@class="next"]/@href').extract_first()
        print(next_url_temp)
        if next_url_temp is not None:
            next_url = 'https://www.guazi.com' + next_url_temp
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                cookies=self.cookies,
            )

    # 解析详情页
    def parse_car(self, response):
        time.sleep(0.7)
        item = response.meta['item']
        item['所在城市'] = response.xpath('//p[@class="city-curr"]/text()').extract_first().replace(' ', '').replace('\n', '')
        item['上牌时间'] = response.xpath('//li[@class="one"]/span/text()').extract_first()
        item['表显里程'] = response.xpath('//li[@class="two"]/span/text()').extract_first()
        item['车辆品牌'] = response.xpath('//div[@class="left-nav"]/a[3]/text()').extract_first()[2:-3]
        item['过户次数'] = response.xpath('//li[@class="seven"]/div/text()').extract_first()
        item['看车地址'] = response.xpath('//li[@class="eight"]/div/text()').extract_first()
        item['年检到期'] = response.xpath('//li[@class="nine"]/div/text()').extract_first()
        item['交强险'] = response.xpath('//li[@class="ten"]/div/text()').extract_first()
        item['商业险到期'] = response.xpath('//li[@class="last"]/div/text()').extract_first().replace(' ', '')
        item['上牌地'] = response.xpath('//li[@class="three"]/span/text()').extract_first()
        item['新车指导价'] = response.xpath('//span[@class="newcarprice"]/text()').extract_first().replace('\n', '').replace(
            '\r', '').replace(' ', '')[5:]
        item['发动机'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]/tr[4]/td[2]/text()').extract_first()
        item['变速箱'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]/tr[5]/td[2]/text()').extract_first()
        item['车辆级别'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]/tr[3]/td[2]/text()').extract_first()
        item['车身结构'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]/tr[6]/td[2]/text()').extract_first()
        item['燃料类型'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[2]/tr[7]/td[2]/text()').extract_first()
        item['燃油标号'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[2]/tr[8]/td[2]/text()').extract_first()
        item['车辆排量'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[2]/tr[2]/td[2]/text()').extract_first()
        item['驱动方式'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[3]/tr[2]/td[2]/text()').extract_first()
        item['车辆厂商'] = response.xpath(
            '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]/tr[2]/td[2]/text()').extract_first()
        item['车辆图集'] = response.xpath('//ul[@class="det-picside js-picside"]//img/@data-src').extract()
        yield item
