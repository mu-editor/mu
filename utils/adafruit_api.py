"""
The scrapy package must be installed.

Usage:

scrapy runspider adafruit_api.py -o adafruit.json

"""
import scrapy
from bs4 import BeautifulSoup


class AdafruitSpider(scrapy.Spider):
    name = 'AdafruitSpider'
    start_urls = ['https://circuitpython.readthedocs.io/en/2.x/shared-bindings/index.html', ]

    def parse(self, response):
        """
        Scrapes the list of modules associated with CircuitPython. Causes
        scrapy to follow the links to the module docs and uses a different
        parser to extract the API information contained therein.
        """
        for next_page in response.css('div.toctree-wrapper li a'):
            yield response.follow(next_page, self.parse_api)

    def to_dict(self, name, args, description):
        """
        Returns a dictionary representation of the API element if valid, else
        returns None.
        """
        if name.endswith('__'):
            return None
        return {
            'name': name,
            'args': args,
            'description': description,
        }


    def parse_api(self, response):
        """
        Parses a *potential* API documentation page.
        """
        # Find all the function definitions on the page:
        for func in response.css('dl.function'):
            # Class details are always first items in dl.
            func_spec = func.css('dt')[0]
            func_doc = func.css('dd')[0]
            # Function name is always first dt
            fn1 = BeautifulSoup(func_spec.css('code.descclassname').extract()[0],
                                'html.parser').text
            fn2 = BeautifulSoup(func_spec.css('code.descname').extract()[0],
                                'html.parser').text
            func_name = fn1 + fn2
            # Args into function
            args = []
            for ems in func_spec.css('em'):
                args.append(ems.extract().replace('<em>', '').replace('</em>', ''))
            # Function description.
            soup = BeautifulSoup(func_doc.extract(), 'html.parser')
            d = self.to_dict(func_name, args, soup.text)
            if d:
                yield d
        # Find all the class definitions on the page:
        for classes in response.css('dl.class'):
            # Class details are always first items in dl.
            class_spec = classes.css('dt')[0]
            class_doc = classes.css('dd')[0]
            # Class name is always first dt
            cn1 = BeautifulSoup(class_spec.css('code.descclassname').extract()[0],
                                'html.parser').text
            cn2 = BeautifulSoup(class_spec.css('code.descname').extract()[0],
                                'html.parser').text
            class_name = cn1 + cn2
            # Args into __init__
            init_args = []
            for ems in class_spec.css('em'):
                props = 'property' in ems.css('::attr(class)').extract()
                if not props:
                    init_args.append(ems.extract().replace('<em>', '').replace('</em>', ''))
            # Class description. Everything up to and including the field-list.
            soup = BeautifulSoup(class_doc.extract(), 'html.parser')
            contents = soup.contents[0].contents
            description = ''
            for child in contents:
                if child.name == 'p':
                    description += child.text + '\n\n'
                if child.name == 'table':
                    raw = child.text
                    rows = [r.strip() for r in raw.split('/n') if r.strip()]
                    description += '\n'
                    description += '\n'.join(rows)
                    break
                if child.name == 'dl':
                    break
            d = self.to_dict(class_name, init_args, description)
            if d:
                yield d
            # Remaining dt are methods or attributes
            for methods in classes.css('dl.method'):
                # Parse and yield methods.
                method_name = BeautifulSoup(methods.css('code.descname').extract()[0],
                                            'html.parser').text
                if method_name.startswith('__'):
                    break
                method_name = class_name + '.' + method_name
                method_args = []
                for ems in methods.css('em'):
                    method_args.append(ems.extract().replace('<em>', '').replace('</em>', ''))
                description = BeautifulSoup(methods.css('dd')[0].extract(),
                                            'html.parser').text
                d = self.to_dict(method_name, method_args, description)
                if d:
                    yield d
            for data in classes.css('dl.attribute'):
                name = BeautifulSoup(methods.css('code.descname').extract()[0],
                                                 'html.parser').text
                name = class_name + '.' + name
                description = BeautifulSoup(methods.css('dd')[0].extract(),
                                            'html.parser').text
                d = self.to_dict(name, None, description)
                if d:
                    yield d
            for data in classes.css('dl.data'):
                name = BeautifulSoup(methods.css('code.descname').extract()[0],
                                                 'html.parser').text
                name = class_name + '.' + name
                description = BeautifulSoup(methods.css('dd')[0].extract(),
                                            'html.parser').text
                d = self.to_dict(name, None, description)
                if d:
                    yield d

