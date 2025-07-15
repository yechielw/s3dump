{
  description = "s3dump Python utility";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
      in rec {
        packages.default = python.pkgs.buildPythonApplication {
          pname = "s3dump";
          version = "0.1.0";
          format = "pyproject";
          src = self;
          propagatedBuildInputs = with python.pkgs; [ requests tqdm ];

          nativeBuildInputs = with python.pkgs; [ setuptools wheel ];

          checkInputs = with python.pkgs; [ pytest ];
          doCheck = true;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            (python.withPackages (p: with p; [ requests tqdm pytest setuptools wheel ]))
          ];
        };
      });
}
