import scrapy


class IrishJobsSpider(scrapy.Spider):
    name = 'irishjobs'

    start_urls = ['http://www.irishjobs.ie/ShowResults.aspx?Keywords=software']

    def parse(self, response):
        """
        Extracts links to job detail pages and parses them (delegates to parse_job).
        Follows pagination links to next page of search results.
        """

        for href in response.css("a.show-more::attr(href)").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job)

        next_page = response.xpath('//a[text()=">"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_job(self, response):
        """
        Extracts job details
        """

        job_title = response.css('div.job-description h1::text').extract_first()
        location = response.css('li.location::text').extract_first()
        salary = response.css('li.salary::text').extract_first()
        employment_type = response.css('li.employment-type::text').extract_first()
        date_updated = response.css('li.updated-time::text').extract_first()
        job_description = response.xpath(
            '//div[@class="job-details"]/descendant-or-self::text()').extract()
        job_description = " ".join(job_description)
        recruiter = response.xpath('//div[@class="border-wrap"]/h2/text()').extract_first()

        yield {
            'job_title': job_title,
            'location': location,
            'salary': salary,
            'employment_type': employment_type,
            'date_updated': date_updated,
            'job_description': job_description,
            'recruiter': recruiter,
        }
