import { spawnSync } from "node:child_process";

function checkCommand(command, args = ["--version"]) {
  const result = spawnSync(command, args, { encoding: "utf-8", shell: true });
  return result.status === 0;
}

const checks = [
  {
    ok: checkCommand("cargo"),
    failMessage: "Rust/Cargo não encontrado. Instale em: https://rustup.rs/",
  },
  {
    ok: checkCommand("rustc"),
    failMessage: "Rustc não encontrado. Instale em: https://rustup.rs/",
  },
  {
    ok: checkCommand("python"),
    failMessage: "Python não encontrado no PATH.",
  },
];

const failed = checks.filter((c) => !c.ok);
if (failed.length) {
  for (const item of failed) {
    console.error(`- ${item.failMessage}`);
  }
  process.exit(1);
}

console.log("Preflight Tauri OK.");
