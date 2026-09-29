# Publishing

Every push to this repository goes through the organization's GitHub App, so
GitHub credits it to `icra-2027-psf-publisher[bot]`. A push with a personal
login, an edit in the GitHub web editor, or starring, watching or forking the
repository shows that account's username on public pages. Do none of these,
and do not create repositories in the organization.

## Setup (once)

You need your own App key and the App ID, both sent privately, and Python 3
with `pip install "PyJWT[crypto]"`.

```sh
mkdir -p ~/.config/icra-2027-psf-publisher && chmod 700 ~/.config/icra-2027-psf-publisher
# save your key as ~/.config/icra-2027-psf-publisher/private-key.pem, then:
chmod 600 ~/.config/icra-2027-psf-publisher/private-key.pem
echo <APP_ID> > ~/.config/icra-2027-psf-publisher/app_id

git clone https://github.com/icra-2027-psf/icra-2027-psf.github.io.git
cd icra-2027-psf.github.io
git config user.name "Anonymous Authors"
git config user.email "anonymous@icra-2027-psf.invalid"
git config credential.https://github.com.helper ""
git config --add credential.https://github.com.helper "!$(pwd)/.github/publishing/git-credential-app"
```

## Check before the first push

```sh
GIT_TRACE=1 git push --dry-run origin main 2>&1 | grep -E "credential|ssh"
```

Every line printed must name `.github/publishing/git-credential-app`. If
`gh auth`, `git-credential-store`, `osxkeychain`, `manager` or `ssh` appears,
stop: the push would carry your login.

## Publish

Commit and `git push`. GitHub Actions rebuilds the site in about a minute.
