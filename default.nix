{ src ? fetchGit ./., siteURL ? "https://wdtz.org", relativeURLs ? false }:
let
  fetchNixpkgs = import ./nix/fetch-nixpkgs.nix;
  pkgs = import fetchNixpkgs { };
in
  with pkgs;
  assert !relativeURLs -> siteURL != null;
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

  # TODO: Just properly generate the config instead of patching the existing one
  patchPhase = ''
    substituteInPlace publishconf.py \
      --replace "SITEURL = 'https://wdtz.org'" "${lib.optionalString (siteURL != null) "SITEURL = '${siteURL}'"}" \
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
