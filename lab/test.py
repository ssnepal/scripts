'''
Blogger-cli project main file for handling CLI.
'''
__author__ = "Hemanta Sharma (hemanta212 github)"

import click
from config_writer import Config as Cfg
from logger_file import Logger
from cli_utils import Exists, Blog


cfg = Cfg('~/.blogger_cli.cfg', backup_dir='~/.blogger_cli/backup/')
exists = Exists(cfg)
logger_cls = Logger(level='debug', console=False)
logger = logger_cls.get_logger()


@click.group()
def main():
    '''
     A testing project for blogger-cli project
    '''


@main.command()
def hi():
    '''
    A comand test if succesfully installed
    '''
    message = '''
            WELCOME TO BLOGGER_CLI
Blogger cli is succesfully installed and working!

use blogger-cli --help for more info!
    '''
    print(message)


@main.command()
@click.option('--blog', '-b', help='name of the blog')
@click.option('--delete', '-d', help='delte config file')
@click.argument('key', nargs=2)
def config(key, blog, delete):
    '''
    give me a suitable key to store
    '''
    if not blog:
        click.secho("checking for default blog")
    elif blog:
        if exists.blog_exists(blog):
            blog_obj = Blog(cfg, blog)
            if delete:
                response = click.prompt("delete the config file?[y/n]")
                if response.lower == 'y':
                    cfg.delete_config()
                    return 'deleted config file'

            elif key:
                if len(key) == 1:
                    return blog_obj.get(key[0])
                else:
                    blog_attr = cfg.read(key=blog)
                    if key[0] in blog_attr:
                        blog_obj.add_key(key[0], key[1])
                        print("added", key[1], "to", key[0])
                    else:
                        print("Invalid key used")


@main.command()
@click.option('--setup', '-s', help="setup all config values for a blog")
@click.option('--remove', '-rm', help="remove a blog")
@click.option('--add', '-a', help="add a new blog")
@click.option('--listall', '-l', help="args (all,key)")
def blogs(setup, add, remove, listall):
    '''
    Manages blogs setting, adding, removing and listing all blogs.
    '''

    if add:
        # the value of add is a blog name. same other params
        blog_name = add
        blog_obj = Blog(cfg, blog_name)
        if not exists.blog_exists(blog_name):
            blog_obj.register()
            response = click.prompt("Setup this blog's configs now?[y/n]")
            if response.upper == 'Y':
                setup = blog_name
            else:
                print("Registered", blog_name, "succesfully")
        else:
            click.secho("blog already exists")

    if setup:
        blog_name = setup
        if exists.blog_exists(blog_name):
            click.secho("Running a config setup for {0}".format(blog_name))
            blog_obj = Blog(cfg, blog_name)
            blog_attr = cfg.read(key=blog_name)
            for k, v in blog_attr.items():
                value = click.prompt(k, default=v)
                blog_obj.add_key(k, value)
            click.secho("successfully updated configs")

    elif remove:
        blog_name = remove
        blog_obj = Blog(cfg, blog_name)
        if not exists.blog_exists(blog_name):
            print(blog_name, "doesnot exists")
        else:
            click.secho("removing..")
            blog_obj.delete()
            click.secho("Deleted {0}".format(blog_name))

    elif listall:
        blog_name = listall
        for i in Blog.blogs(cfg):
            print(i)
    else:
        click.secho("No option provided")


if __name__ == "__main__":
    main()
