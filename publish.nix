
let
  output = import ./default.nix {};
  inherit (import <nixpkgs> {}) rsync openssh stdenv;
in stdenv.mkDerivation {
  name = "wdtz.org-upload";
  buildInputs = [ rsync openssh ];
  shellHook = ''
    rsync -e ssh -P -rvz ${output}/ will@wdtz.org:~/www/ --cvs-exclude
  '';
}

