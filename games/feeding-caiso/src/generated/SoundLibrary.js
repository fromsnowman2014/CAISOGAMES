
// Generated Sound Library (Web Audio API) - Phase 5: Zen/Ethereal
export const SoundLibrary = {
    throw: (ctx, masterVol) => {
        // Soft whoosh with wind chime tail
        const now = ctx.currentTime;

        // White noise whoosh via filtered oscillator
        const osc = ctx.createOscillator();
        const filter = ctx.createBiquadFilter();
        const gain = ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.08);
        osc.frequency.exponentialRampToValueAtTime(600, now + 0.2);

        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(1000, now);
        filter.Q.setValueAtTime(0.5, now);

        gain.gain.setValueAtTime(0.15 * masterVol, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now);
        osc.stop(now + 0.2);

        // Tiny chime accent
        const chime = ctx.createOscillator();
        const chimeGain = ctx.createGain();
        chime.type = 'sine';
        chime.frequency.setValueAtTime(2093, now + 0.05);
        chimeGain.gain.setValueAtTime(0.08 * masterVol, now + 0.05);
        chimeGain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        chime.connect(chimeGain);
        chimeGain.connect(ctx.destination);
        chime.start(now + 0.05);
        chime.stop(now + 0.3);
    },

    eat: (ctx, masterVol) => {
        // Gentle crystalline absorption
        const now = ctx.currentTime;

        // Soft bell tone
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gain = ctx.createGain();

        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(880, now);
        osc1.frequency.exponentialRampToValueAtTime(1100, now + 0.1);

        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(1320, now);
        osc2.frequency.exponentialRampToValueAtTime(1650, now + 0.1);

        gain.gain.setValueAtTime(0.2 * masterVol, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);

        osc1.start(now);
        osc1.stop(now + 0.35);
        osc2.start(now);
        osc2.stop(now + 0.35);
    },

    combo: (ctx, masterVol) => {
        // Harmonic bells ascending - wind chime cascade
        const now = ctx.currentTime;
        // Pentatonic scale for zen feel: C5, D5, E5, G5
        const freqs = [523.25, 587.33, 659.25, 783.99];

        freqs.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + i * 0.08);

            gain.gain.setValueAtTime(0.12 * masterVol, now + i * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.5);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now + i * 0.08);
            osc.stop(now + i * 0.08 + 0.5);

            // Harmonic overtone for each bell
            const harm = ctx.createOscillator();
            const harmGain = ctx.createGain();
            harm.type = 'sine';
            harm.frequency.setValueAtTime(freq * 2, now + i * 0.08);
            harmGain.gain.setValueAtTime(0.04 * masterVol, now + i * 0.08);
            harmGain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.3);
            harm.connect(harmGain);
            harmGain.connect(ctx.destination);
            harm.start(now + i * 0.08);
            harm.stop(now + i * 0.08 + 0.3);
        });
    },

    fever: (ctx, masterVol) => {
        // Ethereal choir swell with shimmering overtones
        const now = ctx.currentTime;

        // Root chord: C major spread voicing
        const chordFreqs = [261.63, 329.63, 523.25, 659.25];

        chordFreqs.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now);
            // Gentle vibrato
            const lfo = ctx.createOscillator();
            const lfoGain = ctx.createGain();
            lfo.frequency.setValueAtTime(5 + i, now);
            lfoGain.gain.setValueAtTime(3, now);
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            lfo.start(now);
            lfo.stop(now + 1.5);

            gain.gain.setValueAtTime(0.001, now);
            gain.gain.linearRampToValueAtTime(0.12 * masterVol, now + 0.4);
            gain.gain.linearRampToValueAtTime(0.08 * masterVol, now + 1.0);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 1.5);
        });

        // Shimmer: high sine sweep
        const shimmer = ctx.createOscillator();
        const shimGain = ctx.createGain();
        shimmer.type = 'sine';
        shimmer.frequency.setValueAtTime(2000, now);
        shimmer.frequency.exponentialRampToValueAtTime(4000, now + 1.0);
        shimGain.gain.setValueAtTime(0.001, now);
        shimGain.gain.linearRampToValueAtTime(0.05 * masterVol, now + 0.3);
        shimGain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
        shimmer.connect(shimGain);
        shimGain.connect(ctx.destination);
        shimmer.start(now);
        shimmer.stop(now + 1.5);
    },

    gameover: (ctx, masterVol) => {
        // Gentle fade with minor key descent
        const now = ctx.currentTime;

        // Minor chord descent: Am -> Dm feel
        const notes = [
            { freq: 440, start: 0, dur: 1.0 },
            { freq: 329.63, start: 0, dur: 1.2 },
            { freq: 261.63, start: 0.3, dur: 1.0 },
            { freq: 220, start: 0.6, dur: 1.2 }
        ];

        notes.forEach(note => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(note.freq, now + note.start);
            osc.frequency.linearRampToValueAtTime(note.freq * 0.95, now + note.start + note.dur);

            gain.gain.setValueAtTime(0.001, now + note.start);
            gain.gain.linearRampToValueAtTime(0.12 * masterVol, now + note.start + 0.1);
            gain.gain.exponentialRampToValueAtTime(0.001, now + note.start + note.dur);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + note.start);
            osc.stop(now + note.start + note.dur + 0.1);
        });
    },

    levelup: (ctx, masterVol) => {
        // Wind chime cascade - pentatonic ascending
        const now = ctx.currentTime;
        // C pentatonic: C5, D5, E5, G5, A5, C6
        const freqs = [523.25, 587.33, 659.25, 783.99, 880, 1046.50];

        freqs.forEach((f, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(f, now + i * 0.12);

            gain.gain.setValueAtTime(0.15 * masterVol, now + i * 0.12);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.6);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.12);
            osc.stop(now + i * 0.12 + 0.6);

            // Octave harmonic for sparkle
            const harm = ctx.createOscillator();
            const harmGain = ctx.createGain();
            harm.type = 'sine';
            harm.frequency.setValueAtTime(f * 2, now + i * 0.12);
            harmGain.gain.setValueAtTime(0.05 * masterVol, now + i * 0.12);
            harmGain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.4);
            harm.connect(harmGain);
            harmGain.connect(ctx.destination);
            harm.start(now + i * 0.12);
            harm.stop(now + i * 0.12 + 0.4);
        });
    }
};
