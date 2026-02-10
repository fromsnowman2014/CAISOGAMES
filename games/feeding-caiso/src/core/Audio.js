import { SoundLibrary } from '/src/generated/SoundLibrary.js';

export class AudioManager {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterVolume = 0.5;
        this.enabled = true;
    }

    play(key) {
        if (!this.enabled) return;
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        if (SoundLibrary[key]) {
            SoundLibrary[key](this.ctx, this.masterVolume);
        } else {
            console.warn(`Sound '${key}' not found in library.`);
        }
    }
}
