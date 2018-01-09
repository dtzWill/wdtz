{ src ? fetchGit ./., siteURL ? "https://wdtz.org", relativeURLs ? false }:
let
  fetchNixpkgs = import ./nix/fetch-nixpkgs.nix;
  pkgs = import fetchNixpkgs { };
in
  with pkgs;
let
  version = src.shortRev;

  sourceFilter = name: type: let baseName = baseNameOf (toString name); in
    (lib.cleanSourceFilter name type) &&
    !(
      (type == "directory" && (lib.hasPrefix "output" baseName ||
                               lib.hasPrefix "__pycache__" baseName))
     );
in stdenv.mkDerivation {
  name = "wdtz-${version}";
  inherit version;

  src = builtins.filterSource sourceFilter ./.;

  nativeBuildInputs = with python3.pkgs; [ pelican lxml typogrify optipng mozjpeg ];

  patchPhase = ''
    substituteInPlace publishconf.py \
      --replace "SITEURL = 'https://wdtz.org'" "SITEURL = '${siteURL}'" \
      --replace "RELATIVE_URLS = False" "RELATIVE_URLS = ${if relativeURLs then "True" else "False"}"
  '';

  buildPhase = ''
    make clean
    make publish
  '';

  installPhase = ''
    mv output/ $out
  '';
}
