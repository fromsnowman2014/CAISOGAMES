
// Generated Sound Library (Web Audio API) - Phase 4: Neon Arcade
export const SoundLibrary = {
    throw: (ctx, masterVol) => {
        // Retro Jump / Throw - Triangle wave pitch slide
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        const now = ctx.currentTime;

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(350, now);
        osc.frequency.exponentialRampToValueAtTime(600, now + 0.15);

        gain.gain.setValueAtTime(0.3 * masterVol, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);

        osc.start(now);
        osc.stop(now + 0.15);
    },

    eat: (ctx, masterVol) => {
        // Happy Chop - Sine + Noise burst (simulated)
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        const now = ctx.currentTime;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.linearRampToValueAtTime(800, now + 0.05);
        osc.frequency.linearRampToValueAtTime(400, now + 0.15);

        gain.gain.setValueAtTime(0.4 * masterVol, now);
        gain.gain.linearRampToValueAtTime(0.4 * masterVol, now + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);

        osc.start(now);
        osc.stop(now + 0.15);
    },

    combo: (ctx, masterVol) => {
        // Combo Rise - Arpeggio
        const now = ctx.currentTime;
        [440, 554, 659].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.type = 'square';
            osc.frequency.setValueAtTime(freq, now + i * 0.05);

            gain.gain.setValueAtTime(0.15 * masterVol, now + i * 0.05);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.05 + 0.1);

            osc.start(now + i * 0.05);
            osc.stop(now + i * 0.05 + 0.1);
        });
    },

    fever: (ctx, masterVol) => {
        // Fever Start - Power Up Glissando
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gain = ctx.createGain();

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);

        const now = ctx.currentTime;

        // Lead
        osc1.type = 'sawtooth';
        osc1.frequency.setValueAtTime(200, now);
        osc1.frequency.exponentialRampToValueAtTime(880, now + 1.0);

        // Detune harmony
        osc2.type = 'square';
        osc2.frequency.setValueAtTime(202, now);
        osc2.frequency.exponentialRampToValueAtTime(884, now + 1.0);

        gain.gain.setValueAtTime(0.4 * masterVol, now);
        gain.gain.linearRampToValueAtTime(0, now + 1.0);

        osc1.start(now);
        osc1.stop(now + 1.0);
        osc2.start(now);
        osc2.stop(now + 1.0);
    },

    gameover: (ctx, masterVol) => {
        // Game Over - Pitch Down
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        const now = ctx.currentTime;

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(50, now + 1.5);

        gain.gain.setValueAtTime(0.3 * masterVol, now);
        gain.gain.linearRampToValueAtTime(0, now + 1.5);

        osc.start(now);
        osc.stop(now + 1.5);
    },

    levelup: (ctx, masterVol) => {
        // Level Up Fanfare
        const now = ctx.currentTime;
        const freqs = [523.25, 659.25, 783.99, 1046.50]; // C E G C

        freqs.forEach((f, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(f, now + i * 0.1);

            gain.gain.setValueAtTime(0.2 * masterVol, now + i * 0.1);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.1 + 0.4);

            osc.start(now + i * 0.1);
            osc.stop(now + i * 0.1 + 0.4);
        });
    }
};
