FROM python:3-onbuild

CMD [ "python", "-u", "./main.py" ]

EXPOSE 5000
EXPOSE 5001
