
# Setting PATH for Python 3.5
# The orginal version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.5/bin:${PATH}"
export PATH
export EDITOR=emacs
alias racket='/Applications/Racket\ v6.6/bin/racket'
alias emacs="/usr/local/Cellar/emacs/25.1/Emacs.app/Contents/MacOS/Emacs -nw"
export EMACS_SERVER_FILE=~/.emacs.d/server/lightning

# Handy Shortcuts #
alias o=open
alias oe='$EDITOR'
alias bp='open ~/.bash_profile'
alias src="source ~/.bash_profile"
alias ls='ls -g'
alias o=open
alias c=clear
alias h=history
alias j='jobs -l'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'
alias ~='cd ~'

# Safety Nets #

# do not delete / or prompt if deleting more than 3 files at a time #
alias rm='rm -I --preserve-root'

# confirmation #
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'

# Parenting changing perms on / #
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'

# Commands #

alias path='echo -e ${PATH//:/\\n}'
alias now=date

# Network Tools #

# Stop after sending count ECHO_REQUEST packets #
alias ping='ping -c 5'
# Do not wait interval 1 second, go fast #
alias fastping='ping -c 100 -s.2'
alias ports='netstat -tulanp'

# Web Tools #

alias chrome="open -a \"Google Chrome\""
alias github="chrome http://github.com"
alias email="chrome http://inbox.google.com"
alias djs="python manage.py runserver"

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
