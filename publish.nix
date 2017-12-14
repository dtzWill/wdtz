
let
  output = import ./default.nix {};
  fetchNixpkgs = import ./nix/fetch-nixpkgs.nix;
  pkgs = import fetchNixpkgs { };
  inherit (pkgs) rsync openssh stdenv;
in stdenv.mkDerivation {
  name = "wdtz.org-upload";
  buildInputs = [ rsync openssh ];
  shellHook = ''
    rsync -e ssh -P -rvz ${output}/ will@wdtz.org:~/www/ --cvs-exclude
  '';
}

