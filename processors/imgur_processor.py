import click
import sys
import urllib
import os
import time

from imgurpython import ImgurClient

class ImgurProcessor:
    client = ImgurClient('08e2dfe01d7bf32',
                         'ac45838cb6f35c2cb30491657fca0d4cad0a7c60')

    # Log variable for the class
    IMGUR = click.style('[imgur]', fg='blue')

    # static variables needed for the __reporthook
    bar = None
    done_percent = 0

    def __init__(self):
        pass

    @staticmethod
    def __reporthook(count, block_size, total_size):
        ''' Callback function to urllib.urlretrieve to add progress bar '''
        if count is 0:
            ImgurProcessor.bar = click.progressbar(length=100, show_pos=True)
            ImgurProcessor.done_percent = 0
        percent = min(int(count * block_size * 100 / total_size), 100)
        if ImgurProcessor.bar is not None:
            ImgurProcessor.bar.update(percent - ImgurProcessor.done_percent)
            ImgurProcessor.done_percent = percent

        # Move to next line if the file download is complete
        if ImgurProcessor.done_percent == 100:
            click.echo()

    def process(self, url, out):
        url_parts = url.split('/')
        # populate variables
        is_album = 'a' in url_parts or 'gallery' in url_parts
        key = url_parts[-1]

        click.echo('%s is_abum: %s, key: %s' % (ImgurProcessor.IMGUR, is_album, key))
        outname = out if out else key

        if is_album:
            self.__processor_album(key, outname)
        else:
            self.__process_file(url, outname)

    def __process_file(self, url, outname):
        if os.path.exists(outname):
            click.echo(click.style('[imgdl] File already exits. Skipping', fg='yellow'))
        else:
            click.echo('%s Downloading image %s' % (ImgurProcessor.IMGUR, outname))
            urllib.urlretrieve(url, outname, ImgurProcessor.__reporthook)
            click.echo(click.style('[imgdl] Download success. Location: %s' % outname, fg='green'))

    def __processor_album(self, key, outname):
        click.echo('%s Getting image links for the album/gallery' % ImgurProcessor.IMGUR)

        image_links = [x.link for x in ImgurProcessor.client.get_album_images(key)]
        click.echo('%s Fetched %s image link[s] for the album/gallery' % (ImgurProcessor.IMGUR, len(image_links)))

        if not os.path.exists(outname):
            os.makedirs(outname)
        else:
            # Exit if a file of name as referenced by outname exists
            if os.path.isfile(outname):
                click.echo(
                    click.style('[imgur] File %s already exits. Exiting' % outname, fg='yellow'))
                sys.exit(1)

        for link in image_links:
            fullfilename = os.path.join(os.getcwd(), '%s/%s' % (outname, link.split('/')[-1]))
            self.__process_file(link, fullfilename)
