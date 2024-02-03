# Application

Chat application using Websocket with Django + Channels

POC for testing the Websocket Python and Django 

## Development Setup

1. Clone
   `git clone git@github.com:wcipriano/chat-websocket-django.git`
2. Open folder
   `cd chat-websocket-django`
3. Create python virtual env:
   `python3.9 -m venv .venv`
4. Activate venv
   `source ./.venv/bin/activate`
5. Install libraries
   `pip install -r requirements.txt`
6. Create file `.env` into root dir `vim .env`
   ```
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
   SECRET_KEY=9b28on)#g5&dxdi*pc7gwiw4ep1-b(m(zza!kq#@z*s2%(s7p=
   RENDER_EXTERNAL_HOSTNAME=
   DATABASE_URL=
   ```
   Without "DATABASE_URL" param it will create a "db.sqlite3" DB in the root dir
   RENDER_EXTERNAL_HOSTNAME it needed only in test or production env

7. Run script build 
   `./build.sh`

8. Create django super user
   `python manage.py createsuperuser`

9. Run command to start application

`daphne --port 8000 --bind 0.0.0.0 dj_channels.asgi:application` or
`python manage.py runserver localhost:8000`

10. Open App in the browser and have fun   \o/ \o/ \o/
http://localhost:8000/chat/sala1/

11. 



## @TODO:
- Use render.yaml for Deploys: [Link](https://docs.render.com/deploy-django#use-renderyaml-for-deploys)
- Change `channels.layers.InMemoryChannelLayer` to `channels_redis.core.RedisChannelLayer`
- 

## REFs

### Django Channels
- [Django Channels Doc](https://channels.readthedocs.io/en/stable/index.html)
- [Introduction to Django Channels](https://testdriven.io/blog/django-channels/)
- [Getting Started with Django Channels](https://realpython.com/getting-started-with-django-channels/)
- [Introduction to Django Channels and WebSockets](https://medium.com/@adabur/introduction-to-django-channels-and-websockets-cb38cd015e29)
- 

### Deploy Render
- [Deploy Your Django App: A Step-by-Step Guide with Render](https://medium.com/django-unleashed/deploy-your-django-app-with-ease-a-step-by-step-guide-with-render-810ccbf49573)
- [Getting Started with Django on Render](https://docs.render.com/deploy-django#use-renderyaml-for-deploys)
- [Deploy django-channels to render.com](https://community.render.com/t/deploy-django-channels-to-render-com/1011/9)
- 

### Static files Development X Production
- Django Doc: How to manage static files: [link](https://docs.djangoproject.com/en/5.0/howto/static-files/)
- Django Doc: How to deploy static files: [link](https://docs.djangoproject.com/en/5.0/howto/static-files/deployment/)
- StackOverflow: Django - Static file not found: [link](https://stackoverflow.com/questions/6014663/django-static-file-not-found)
- Django Static Files and Templates: [link](https://learndjango.com/tutorials/django-static-files-and-templates)
- WhiteNoise is an easy way to serve static files: [link](https://whitenoise.readthedocs.io/en/latest/)
- a



# @TODO Implementação UaiAds 

1. **Teste desacoplado WS/Http** ✅

   Criar view que recebe uma requisição via http e enviar uma mensagem para uma sala via websocket:
   - /chat/<str:room_name>/send-test/

2. **POC**:

   Inserir POC no projeto UAIAds (teste websocket funcionando)

3. **Teste timeout** - Cliente não responde.  ✅

   Após estabelecida a conn WS, se o server perde a conexão com o client, existe um timeout no componente channels que remove os "clientes isolados" automaticamete.
   Assim evita que continue tentando enviar novas mensagens para os mesmos
 
4. Ideias implementação pagamento:
 - Nomenclatura do grupo `"pagamento_<id_pgto>"`
   Usuários que estiverem acompanhando este pagamento entram neste grupo (poode ser mais de um, mas isso é transparente para o server)

5. 

