# This file must be used with ". bin/activate.fish" *from fish* (http://fishshell.org)
# you cannot run it directly

function deactivate --description 'Exit virtualenv and return to normal shell environment'
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
#    if test -n "$_OLD_VIRTUAL_CARGOHOME"
    set -gx CARGO_HOME $_OLD_VIRTUAL_CARGOHOME
    set -e _OLD_VIRTUAL_CARGOHOME
#    end
#    if test -n "$_OLD_VIRTUAL_RUSTUP_HOME"
    set -gx RUSTUP_HOME $_OLD_VIRTUAL_RUSTUP_HOME
    set -e _OLD_VIRTUAL_RUSTUP_HOME
#    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
        functions -e fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
    end

    set -e VIRTUAL_ENV
    if test "$argv[1]" != "nondestructive"
        # Self destruct!
        functions -e deactivate
    end
end

# unset irrelevant variables
deactivate nondestructive

set -gx VIRTUAL_ENV %{VENV_DIRECTORY}%

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH
set -gx PATH "$VIRTUAL_ENV/.cargo/bin" $PATH

# unset CARGOHOME if set
#if set -q CARGO_HOME
set -gx _OLD_VIRTUAL_CARGOHOME $CARGO_HOME
#end
set -gx CARGO_HOME %{VENV_DIRECTORY}%/.cargo

#if set -q RUSTUP_HOME
set -gx _OLD_VIRTUAL_RUSTUP_HOME $RUSTUP_HOME
#end
set -gx RUSTUP_HOME %{VENV_DIRECTORY}%/.rustup

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # fish uses a function instead of an env var to generate the prompt.

    # save the current fish_prompt function as the function _old_fish_prompt
    functions -c fish_prompt _old_fish_prompt

    # with the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command
        set -l old_status $status

        # Prompt override?
        if test -n "(%{VENV_NAME}%) "
            printf "%s%s" "(%{VENV_NAME}%) " (set_color normal)
        else
            # ...Otherwise, prepend env
            set -l _checkbase (basename "$VIRTUAL_ENV")
            if test $_checkbase = "__"
                # special case for Aspen magic directories
                # see http://www.zetadev.com/software/aspen/
                printf "%s[%s]%s " (set_color -b blue white) (basename (dirname "$VIRTUAL_ENV")) (set_color normal)
            else
                printf "%s(%s)%s" (set_color -b blue white) (basename "$VIRTUAL_ENV") (set_color normal)
            end
        end

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
end
