// `npm run dev`: API serverini (4000) və Vite-i (3000) birlikdə işə salır. Windows, macOS və Linux-da işləyir.
import { spawn } from 'node:child_process';

const procs = [
  spawn(process.execPath, ['--watch', '--disable-warning=ExperimentalWarning', 'server/index.js'], {
    stdio: 'inherit',
  }),
  spawn('npx', ['vite', '--port=3000', '--host=0.0.0.0'], { stdio: 'inherit', shell: true }),
];

const stop = () => {
  procs.forEach((p) => p.kill());
  process.exit();
};
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
procs.forEach((p) => p.on('exit', (code) => code && stop()));
