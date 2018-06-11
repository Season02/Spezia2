class Element:
    # par_list = ['author', 'content_url', 'cover', 'digest']

    author = ""
    content_url = ""
    cover = ""
    digest = ""
    title = ""
    publicTime = ""
    url = ""

    def print(self):
        print("author: " + self.author)
        print("content_url: " + self.content_url)
        print("cover: " + self.cover)
        print("digest: " + self.digest)
        print("title: " + self.title)
        print("publicTime: " + self.publicTime)
        print("url: " + self.url)

    # @property
    # def author(self):
    #     return self._author
    #
    # @property
    # def content_url(self):
    #     return self._content_url
    #
    # @property
    # def cover(self):
    #     return self._cover
    #
    # @property
    # def digest(self):
    #     return self._digest