import webapp2
import os
import jinja2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from google.appengine.api import users

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd()))

class RequestPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('home.html')
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
        }
        self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/',RequestPage)],
                                        debug=True)
CLIENT_SECRETS_FILE = "VKSBiJwT7FWDzdKgBoPbD06h"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))


# Call the API's channels.update method to update an existing channel's default language,
# and localized description in a specific language.
def set_channel_localization(youtube, channel_id, default_language, language, description):
  results = youtube.channels().list(
    part="brandingSettings,localizations",
    id=channel_id
  ).execute()

  channel = results["items"][0]
  # Ensure that a value is set for the resource's snippet.defaultLanguage property.
  # To set the snippet.defaultLanguage property for a channel resource,
  # you actually need to update the brandingSettings.channel.defaultLanguage property.
  channel["brandingSettings"]["channel"]["defaultLanguage"] = default_language
  if "localizations" not in channel:
    channel["localizations"] = {}
  channel["localizations"][language] = {
    "description": description
  }

  update_result = youtube.channels().update(
    part="brandingSettings,localizations",
    body=channel
  ).execute()

  localization = update_result["localizations"][language]

  print ("Updated channel '%s' default language to '%s', localized description"
         " to '%s' in language '%s'" % (channel_id, localization["description"], language))


# Call the API's channels.list method to retrieve an existing channel localization.
# If the localized text is not available in the requested language,
# this method will return text in the default language.
def get_channel_localization(youtube, channel_id, language):
  results = youtube.channels().list(
    part="snippet",
    id=channel_id,
    hl=language
  ).execute()

  # The localized object contains localized text if the hl parameter specified
  # a language for which localized text is available. Otherwise, the localized
  # object will contain metadata in the default language.
  localized = results["items"][0]["snippet"]["localized"]

  print "Channel description is '%s' in language '%s'" % (localized["description"], language)


# Call the API's channels.list method to list the existing channel localizations.
def list_channel_localizations(youtube, channel_id):
  results = youtube.channels().list(
    part="snippet,localizations",
    id=channel_id
  ).execute()

  localizations = results["items"][0]["localizations"]

  for language, localization in localizations.iteritems():
    print "Channel description is '%s' in language '%s'" % (localization["description"], language)


if __name__ == "__main__":
  # The "action" option specifies the action to be processed.
  argparser.add_argument("--action", help="Action")
  # The "channel_id" option specifies the ID of the selected YouTube channel.
  argparser.add_argument("--channel_id",
    help="ID for channel for which the localization will be applied.")
  # The "default_language" option specifies the language of the channel's default metadata.
  argparser.add_argument("--default_language", help="Default language of the channel to update.",
    default="en")
  # The "language" option specifies the language of the localization that is being processed.
  argparser.add_argument("--language", help="Language of the localization.", default="de")
  # The "description" option specifies the localized description of the chanel to be set.
  argparser.add_argument("--description", help="Localized description of the channel to be set.",
    default="Localized Description")

  args = argparser.parse_args()

  if not args.channel_id:
    exit("Please specify channel id using the --channel_id= parameter.")

  youtube = get_authenticated_service(args)
  try:
    if args.action == 'set':
      set_channel_localization(youtube, args.channel_id, args.default_language, args.language, args.description)
    elif args.action == 'get':
      get_channel_localization(youtube, args.channel_id, args.language)
    elif args.action == 'list':
      list_channel_localizations(youtube, args.channel_id)
    else:
      exit("Please specify a valid action using the --action= parameter.")
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  else:
    print "Set and retrieved localized metadata for a channel."
