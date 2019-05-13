# typeset

**typeset** is a Flask app exposing my Pandoc setup over the network in order to
typeset documents from the iPad. I write in [Drafts][drafts] and use
[Shortcuts][shortcuts] to talk with typeset.

Runs in production in a [Ubuntu 19.04 Digital Ocean droplet][do] on a free
domain with SSL. Follow [Digital Ocean's guide][guide] in order to deploy the
app with Gunicorn and Nginx, get a free domain with Freenom, and a free
certificate from Let's Encrypt.

## Install and use

1. `git clone git@github.com:apas/typeset.git`
1. `virtualenv env`
1. `source env/bin/activate`
1. `pip install -r requirements.txt`
1. `source env-var`
1. `python flask run`

Note: `python flask run` runs a development server over port 5000. Do not use in
production. Use Gunicorn and Nginx in order to deploy to production.

typeset requires `pandoc`, `pandoc-citeproc`, `pandoc-crossref`,
`pandoc-sidenote`, and `TexLive`. All dependencies are available on
[Linuxbrew][brew] but for `pandoc-sidenote` which is available on
[cabal][cabal]. The first time pandoc will convert to PDF during testing TexLive
will complain about missing dependencies—just install them with `tlmgr`.

## iOS Shortcut

`URL` with the domain and `/md/` endpoint to `Get Contents of URL` which makes a
POST request with request body `Form` and key `file`, value `Shorcut Input`
Magic Variable. `URL` with the domain and `/pdf/` endpoint to `Get Contents of
URL` which makes a GET to `Quick Look`.

## License

MIT

[drafts]:
    https://getdrafts.com

[shortcuts]:
    https://itunes.apple.com/us/app/shortcuts/id915249334?mt=8

[do]:
    https://m.do.co/c/1fb65d2407a3

[guide]:
    https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

[brew]:
    https://docs.brew.sh/Homebrew-on-Linux

[cabal]:
    https://www.haskell.org/cabal/
