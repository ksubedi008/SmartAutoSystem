If your friends are at THEIR homes (Different WiFi)
If your friends are far away, you need a "tunnel" to the internet. The best free tool for this is ngrok.
Download ngrok: Go to ngrok.com, sign up (it's free), and follow the Linux setup instructions.
Run ngrok: In a new terminal, type:
    ngrok http 8000
Get the Link: You will see a "Forwarding" line with a weird web address (like https://random-name.ngrok-free.app).
Update Settings: Add that weird address to your ALLOWED_HOSTS in settings.py (or just use ['*'] like above).
Share: Send that https://... link to your friends. They can access your site from anywhere in the world!