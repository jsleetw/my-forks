from fabric.api import run, env
from fabric.context_managers import settings, cd

my_forks = {
        "django": {"origin": "git@github.com:jsleetw/django.git", "upstream": "git://github.com/django/django.git"},
        "ThinkUp": {"origin": "git@github.com:jsleetw/ThinkUp.git", "upstream": "git://github.com/ginatrapani/ThinkUp.git"},
        "aptsync": {"origin": "git@github.com:jsleetw/aptsync.git", "upstream": "git://github.com/t9md/aptsync.git"},
        "pfff": {"origin": "git@github.com:jsleetw/pfff.git", "upstream": "git://github.com/facebook/pfff.git"},
        "tomahawk": {"origin": "git@github.com:jsleetw/tomahawk.git", "upstream": "git://github.com/oinume/tomahawk.git"},
        "gitflow": {"origin": "git@github.com:jsleetw/gitflow.git", "upstream": "git://github.com/nvie/gitflow.git", "branch": "develop"},
        "git-extras": {"origin": "git@github.com:jsleetw/git-extras.git", "upstream": "git://github.com/visionmedia/git-extras.git"},
        "fabric": {"origin": "git@github.com:jsleetw/fabric.git", "upstream": "git://github.com/fabric/fabric.git"},
        "ssh": {"origin": "git@github.com:jsleetw/ssh.git", "upstream": "git://github.com/bitprophet/ssh.git"},
        "python-mode": {"origin": "git@github.com:jsleetw/python-mode.git", "upstream": "git://github.com/klen/python-mode.git"},
        "oh-my-zsh": {"origin": "git@github.com:jsleetw/oh-my-zsh.git", "upstream": "git://github.com/robbyrussell/oh-my-zsh.git"},
        "django-startproject": {"origin": "git@github.com:jsleetw/django-startproject.git", "upstream": "git://github.com/lincolnloop/django-startproject.git"},
        "git-flow-completion": {"origin": "git@github.com:jsleetw/git-flow-completion.git", "upstream": "git://github.com/bobthecow/git-flow-completion.git"},
        "vim_bridge": {"origin": "git@github.com:jsleetw/vim_bridge.git", "upstream": "git://github.com/nvie/vim_bridge.git"},
        }

code_dir = '~/test_my_forks/'
env.hosts = ["localhost"]


def update():
    for element in my_forks.keys():
        project = element
        origin = my_forks[element]["origin"]
        upstream = my_forks[element]["upstream"]
        if "branch" in my_forks[element]:
            branch = my_forks[element]["branch"]
        else:
            branch = "master"
        with settings(warn_only=True):
            if run("test -d %s%s" % (code_dir, project)).failed:
                run("git clone %s %s%s" % (origin, code_dir, project))
        with cd("%s%s" % (code_dir, project)):
            with settings(warn_only=True):
                run("git remote add upstream %s" % upstream)
            run("git fetch upstream")
            run("git checkout %s" % branch)
            run("git rebase upstream/%s" % branch)
            run("git push origin %s" % branch)
