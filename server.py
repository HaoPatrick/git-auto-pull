from flask import Flask, request
import json, hmac, hashlib, subprocess

from config import config

app = Flask(__name__)


@app.route('/github', methods=['POST', 'GET', 'OPTIONS'])
def github_hook():
  if request.method == 'POST':
    # load project config according to the post data
    request_data = request.data.decode('utf-8')
    try:
      request_data = json.loads(request_data)
    except Exception as e:
      return "Json parse error, are you sure you're using json?", 500
    
    try:
      project_name = request_data['repository']['name']
      project_conf = config[project_name]
    except Exception as e:
      return 'We do not have such repo yet', 500
    
    if project_conf['url'] != request_data['repository']['html_url']:
      return 'Not a chance', 403
    
    # check secret
    signature = hmac.new(project_conf['secret'].encode('utf-8'),
                         request.data, hashlib.sha1).hexdigest()
    if hmac.compare_digest(signature,
                           request.headers.get('X-Hub-Signature').split('=')[1]):
      ret_code = subprocess.call(['git', 'reset', '--hard', 'HEAD'])
      ret_code += subprocess.call(['git', '-C', project_conf['path'], 'pull', 'origin', 'master'])
      if ret_code != 0:
        return 'Oops, your broken git!', 500
      return 'OK, I got it', 200
    else:
      return 'Not a chance', 403
  else:
    return 'Not for today', 403


if __name__ == '__main__':
  app.run()
