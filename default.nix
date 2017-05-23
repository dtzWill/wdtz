{ fetchFromGitHub ? (import <nixpkgs> {}).fetchFromGitHub,
# https://github.com/NixOS/nixpkgs/pull/26030
 nixpkgs ? fetchFromGitHub {
   owner = "NixOS";
   repo = "nixpkgs";
   rev = "330dee016da8b56cba87afa5710a0ec2f8e26372";
   sha256 = "15h4rjm8gbwyx87z2mb744b97mwyv003hi7armpzm4ys2d4f9zh3";
 }
}:
with import nixpkgs {};

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

  nativeBuildInputs = with python3.pkgs; [ pelican lxml typogrify optipng mozjpeg ];

  buildPhase = ''
    make clean
    make publish
  '';

  installPhase = ''
    mv output/ $out
  '';
}
