import click
import sys
import validators
import urllib
import os
import time
from imgurpython import ImgurClient

client_id = '08e2dfe01d7bf32'
client_secret = 'ac45838cb6f35c2cb30491657fca0d4cad0a7c60'

client = ImgurClient(client_id, client_secret)
bar = None
done_percent = 0

@click.command()
@click.argument('url', type=click.STRING, required=True)
@click.argument('out', type=click.Path(), default=None, required=False)
def imgdl(url, out):
    """This script greets you"""
    provider = url_parser(url)

    if (provider == 'IMGUR'):
        imgur_processor(url, out)

def url_parser(url):
    click.echo('[imgdl] Validating url...')
    is_valid = validators.url(url)

    # Exit if url is not valid
    if not is_valid:
        click.echo(click.style('[imgdl] Url is not valid. Exiting', fg='red'))
        sys.exit(1)

    url_parts = url.split('/')
    if 'imgur.com' in url_parts or 'i.imgur.com' in url_parts:
        return 'IMGUR'
    else:
        click.echo(click.style('[imgdl] Only supports imgur.com', fg='red'))
        sys.exit(1)

def reporthook(count, block_size, total_size):
    global bar, done_percent
    if count is 0:
        bar = click.progressbar(length=100, show_pos=True)
        done_percent = 0
    percent = min(int(count * block_size * 100 / total_size), 100)
    if bar is not None:
        bar.update(percent - done_percent)
        done_percent = percent
    if done_percent == 100:
        click.echo()



def imgur_processor(url, out):
    imgur_log_text = click.style('[imgur]', fg='blue')
    url_parts = url.split('/')
    # populate variables
    is_album = 'a' in url_parts or 'gallery' in url_parts
    key = url_parts[-1]

    click.echo('%s is_abum: %s, key: %s' % (imgur_log_text, is_album, key))

    try:
        click.echo('%s Downloading webpage' % imgur_log_text)

        outname = out if out else key
        if (is_album):
            global client
            click.echo('%s Getting image links for the album/gallery' % imgur_log_text)
            image_links = [x.link for x in client.get_album_images(key)]
            click.echo('%s Fetched %s image link[s] for the album/gallery' % (imgur_log_text, len(image_links)))
            if os.path.exists(outname):
                click.echo(click.style('[imgdl] File/directory already exits. Exiting', fg='green'))

            else:
                os.makedirs(outname)
                #with click.progressbar(image_links) as bar_items:
                for link in image_links:
                    fullfilename = os.path.join(os.getcwd(), outname + '/' + link.split('/')[-1])
                    imgur_processor(link, fullfilename)
        else:
            if os.path.exists(outname):
                click.echo(click.style('[imgdl] File already exits. Skipping', fg='green'))
            else:
                click.echo('%s Downloading image %s' % (imgur_log_text, outname))
                urllib.urlretrieve(url, outname, reporthook)
                click.echo(click.style('[imgdl] Download success. Location: %s' % outname, fg='green'))

    except:
        click.echo(click.style('[imgur] Webpage not found', fg='red'))
        raise
        #sys.exit(1)
