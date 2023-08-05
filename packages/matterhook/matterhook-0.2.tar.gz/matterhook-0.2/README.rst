**********
matterhook
**********

Simply send messages to your Mattermost team using `incoming webhooks <http://docs.mattermost.com/developer/webhooks-incoming.html>`_.

Getting the API key
===================
- Login to your Mattermost team site and go to **Account Settings -> Integrations**
- Next to **Incoming Webhooks** click **Edit**
- Select the channel or private group to receive webhook payloads, then click **Add** to create the webhook
- The API key is the last part of the URL (eg: u2x8rkfugj8zbqby9pw3huqnyc)

Usage
=====
Basic usage
-----------
**matterhook** is very simple and efficient to use:

.. code-block:: python

    from matterhook import Webhook

    # mandatory parameters are url and your webhook API key
    mwh = Webhook('https://mattermost.MYCOMPANY.com', 'API_KEY')

    # send a message to the API_KEY's channel
    mwh.send('coconut webhook message')

Advanced usage
--------------

.. code-block:: python

    from matterhook import Webhook

    # mandatory parameters are url and your webhook API key
    mwh = Webhook('https://mattermost.MYCOMPANY.com', 'API_KEY')

    # personalized bot name and icon
    mwh.username = 'cocobot'
    mwh.icon_url = 'http://3.bp.blogspot.com/-bEcLJDp_u7o/UJKPRGazv6I/AAAAAAAABGY/75z_6bbegao/s1600/coconut-oil-alzheimers-study.jpg'

    # send a message to the specified channel
    mwh.send('coconut is da thruth', channel='special_channel')

    # override the username for this message
    mwh.send('secret message', channel='special_channel', username='secret_user')

    # for convenience, you can also do this...
    mwh['incredible_channel'] = 'incredible message'

    # ...and even this
    mwh['incredible_channel'] = {'text': 'incredible message', username='incredible user'}

    # or create fancy messages using attachments (https://docs.mattermost.com/developer/message-attachments.html)
    attachments = []
    message = {}
    message['color'] = '#88fc03'
    message['image_url'] = 'https://about.mattermost.com/wp-content/uploads/2017/08/Mattermost-Logo-Blue.svg'
    message['fallback'] = 'A fallback message'
    markdown_msg = '#### Title\n'
    markdown_msg += 'This is a line of text\n'
    markdown_msg += 'All markdown syntax works in attachments, like tables :\n'
    markdown_msg += '''
    | name                               |   date |
    |------------------------------------|--------|
    | Monty Python and the Holy Grail    |   1975 |
    | Monty Python's Life of Brian       |   1979 |
    | Monty Python's The Meaning of Life |   1983 |
    '''
    message['text'] = markdown_msg
    attachments.append(message)
    mwh.send(attachments=attachments)