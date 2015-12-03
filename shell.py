__author__ = 'nick'
import os, sys, platform, subprocess
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
 
ipaddr = "192.168.43.83"
port = '4200'


class MyHandler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        try:
            print self.path[:15]
            if self.path[:] == '/index.html':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(
                    '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web Shell</title>
    <script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="//cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js"
        type="text/javascript"></script>
    <script >
    /* Created by nick on 12/2/15.*/
 
 
    $(document).ready(function () {
        $('#commandForm').on('submit', function(e) {
            e.preventDefault();
            $.ajax({
                url : 'http://''' + ipaddr + ''':''' + port + '''/commander/run' + window.location.search,
                type: "GET",
                data: $(this).serialize(),
                success: function (data) {
                    var newHistory = document.createElement('p');
                    newHistory.innerHTML = data;
                    document.getElementById('commandHistory').appendChild(newHistory);
                    $("#commandHistory").scrollTop($("#commandHistory")[0].scrollHeight);
                },
                error: function (jXHR, textStatus, errorThrown) {
                    alert('wut');
                }
            });
        });
    });
 
    function getOS(){
    $.ajax({
        url:"http://''' + ipaddr + ''':''' + port + '''/commander/OS",
        success:function(data){
            document.getElementById("OSINFO").innerHTML = data;
        }
    });
}
 
function getUser(){
    {
    $.ajax({
        url:"http://''' + ipaddr + ''':''' + port + '''/commander/user",
        success:function(data){
            document.getElementById("USERINFO").innerHTML = data;
        }
    });
}
}
function init(){
 getOS();
 getUser();
 
 
}
    cheet('up up down down left right left right b a enter', function () {
    document.getElementById('konami').style.display = "inline";
   });
    </script>
    <link type="text/css" href="Styles.css">
</head>
<body onload="init()">
<div style="height: 8%; width: 59.7%; border: 1px solid #ccc; position: absolute; left: 0; top: 0; ">
    &nbsp;OS Info: <div id="OSINFO" style="display: inline"></div>
    <br>
    &nbsp;Current User: <div id="USERINFO" style="display: inline"></div>
</div>
<div style="position: absolute; top: 10%;">
    <form id="commandForm" action="http://''' + ipaddr + ''':800/commander/run" >
        <label>
            Command
        <input type="text" name="command">
        <input type="submit" name="submit" class="button" id="submit_btn" value="send">
        </label>
    </form>
</div>
<br> <br>
 
<div id="konami" style="width: 59.7%; position: absolute; top: 20%; left: 15px; display: none;">
<img src="http://cdn.smosh.com/sites/default/files/ftpuploads/bloguploads/0413/funny-nigel-thornberry-gifs-nyan-cat.gif" style="display: inline; height: 315px">
<img src="https://49.media.tumblr.com/a312646c56615bcdd5e31c22b24fa2e0/tumblr_mkjifpf3Qv1s1vt4mo1_500.gif" style="display: inline; height: 315px">
</div>
 
<!--History on the right side-->
<div id="commandHistory" style="height: 100%; width: 40%; border: 1px solid #ccc; overflow: auto; position: absolute; right: 0;top:0;">
Command History:</div>
</body>
</html>
                    '''
                )
 
            elif self.path[:16] == '/commander/user':
                userhome = os.path.expanduser('~')
                user = os.path.split(userhome)[-1]
                self.send_response(200)
                print "user is " + str(user)
                self.end_headers()
                self.wfile.write(user)
 
 
            elif self.path[:14] == '/commander/OS':
                returnMessage = str(sys.platform) + "\n" + str(platform.platform())
                print(returnMessage)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(returnMessage)
                return
 
 
            elif self.path[:14] == '/commander/run':
                print 'in run'
                fullurl = r'http://'+ ipaddr + ''':''' + port + self.path
                parsed = urlparse.urlparse(fullurl)
                command = urlparse.parse_qs(parsed.query)['command'][0]
                print "command is " + command
                commandOutput = subprocess.check_output([command], shell=True)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(command + ":\n" + commandOutput)
 
 
            else:
                pass
            return
        except Exception as e:
            print e.message
            return
 
if __name__ == '__main__':
    server = HTTPServer((ipaddr, int(port)), MyHandler)
    print 'server probably started'
    server.serve_forever()