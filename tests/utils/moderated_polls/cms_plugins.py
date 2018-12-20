from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import PollPlugin


@plugin_pool.register_plugin
class PollPluginBase(CMSPluginBase):
    model = PollPlugin
    name = 'Poll'
    allow_children = True
    render_template = 'polls/poll.html'

