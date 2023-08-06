"""
Main plugin module 
"""
#import json

from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType
from bs4 import BeautifulSoup

from . import pyjs

class MarkdownMermaidPlugin(BasePlugin):
    """
    Plugin for interpreting Mermaid code
    """
    config_scheme = (

        ('foo', PluginType(str, default='hello')),
        ('arguments', PluginType(dict, default={}))
    )

    def config(self):
        "The plugin's specific configuration (under plugin > markdownmermaid2)"
        return self._config

    def on_config(self, config):
        """
        The initial configuration
        """
        # the plugin config is there
        self._config = config
        mermaid_args = self.config['arguments']
        print("[MERMAID] %s" % mermaid_args)
        

    def on_post_page(self, output_content, config, **kwargs):
        "Generate the HTML code for all code items marked as 'mermaid'"
        # print("--RAW--\n", output_content, "\n------")
        soup = BeautifulSoup(output_content, 'html.parser')
        mermaids = soup.find_all("div", class_="mermaid")
        has_mermaid = bool(len(mermaids))
        # print("PROCESSING MERMAID (%s)" % len(mermaids))

        if has_mermaid:
            new_tag = soup.new_tag("script")
            # get the additional configuration:
            mermaid_args = self.config['arguments']
            assert isinstance(mermaid_args, dict)
            # initialization command
            js_args =  pyjs.dumps(mermaid_args) 
            # print("Javascript args:", js_args)
            new_tag.string="mermaid.initialize(%s);" % js_args
            soup.body.append(new_tag)
            
        return str(soup)