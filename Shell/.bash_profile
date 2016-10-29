
# Setting PATH for Python 3.5
# The orginal version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.5/bin:${PATH}"
export PATH
alias racket='/Applications/Racket\ v6.6/bin/racket'
alias emacs='/usr/bin/emacs'
#alias emacs="/usr/local/Cellar/emacs/25.1/Emacs.app/Contents/MacOS/Emacs -nw"
export EDITOR=emacs
export EMACS_SERVER_FILE=~/.emacs.d/server/lightning

# Handy Shortcuts #
alias o=open
alias oe='$EDITOR'
alias bp='$EDITOR --no-window-system  ~/.bash_profile'
alias src="source ~/.bash_profile"
alias ls='ls -g'
alias l='ls'
alias o=open
alias c=clear
alias h=history
alias x=exit
alias g=git
alias j='jobs -l'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'
alias ~='cd ~'

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
alias gh="chrome http://github.com/davemachado"
alias email="chrome http://inbox.google.com"
alias djs="python manage.py runserver"

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
