with import <nixpkgs> {};

let
  gitrev = lib.commitIdFromGitRepo ./.git;
  gitshort = builtins.substring 0 7 gitrev;
  version = gitshort;

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

  nativeBuildInputs = with python.pkgs; [ pelican lxml typogrify optipng mozjpeg ];

  buildPhase = ''
    make clean
    make publish
  '';

  installPhase = ''
    mv output/ $out
  '';
}
