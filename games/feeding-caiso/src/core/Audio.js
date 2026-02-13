import { SoundLibrary } from '../generated/SoundLibrary.js';

export class AudioManager {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterVolume = 0.5;
        this.enabled = true;

        // Master gain node
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = this.masterVolume;
        this.masterGain.connect(this.ctx.destination);

        // Reverb (ConvolverNode)
        this.convolver = null;
        this.reverbLevel = 0;
        this.reverbGain = this.ctx.createGain();
        this.reverbGain.gain.value = 0;
        this.reverbGain.connect(this.masterGain);

        this._initReverb();
    }

    async _initReverb() {
        try {
            const sampleRate = this.ctx.sampleRate;
            const length = sampleRate * 2;
            const buffer = this.ctx.createBuffer(2, length, sampleRate);

            for (let ch = 0; ch < 2; ch++) {
                const data = buffer.getChannelData(ch);
                for (let i = 0; i < length; i++) {
                    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2.5);
                }
            }

            this.convolver = this.ctx.createConvolver();
            this.convolver.buffer = buffer;
            this.convolver.connect(this.reverbGain);
        } catch (e) {
            console.warn('Reverb init failed:', e.message);
        }
    }

    setReverbLevel(level) {
        this.reverbLevel = level;
        this.reverbGain.gain.setTargetAtTime(level * 0.5, this.ctx.currentTime, 0.1);
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
