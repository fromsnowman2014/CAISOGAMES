// Generated Sound Library (Web Audio API) - Phase 6: Hollow Knight / Cave Atmosphere
export const SoundLibrary = {
    throw: (ctx, masterVol) => {
        // Sharp cave-echo whoosh
        const now = ctx.currentTime;

        const osc = ctx.createOscillator();
        const filter = ctx.createBiquadFilter();
        const gain = ctx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.06);
        osc.frequency.exponentialRampToValueAtTime(200, now + 0.2);

        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(600, now);
        filter.Q.setValueAtTime(1.5, now);

        gain.gain.setValueAtTime(0.18 * masterVol, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);

        // Echo tail
        const echo = ctx.createOscillator();
        const echoGain = ctx.createGain();
        echo.type = 'sine';
        echo.frequency.setValueAtTime(300, now + 0.15);
        echo.frequency.exponentialRampToValueAtTime(150, now + 0.5);
        echoGain.gain.setValueAtTime(0.05 * masterVol, now + 0.15);
        echoGain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        echo.connect(echoGain);
        echoGain.connect(ctx.destination);
        echo.start(now + 0.15);
        echo.stop(now + 0.5);
    },

    eat: (ctx, masterVol) => {
        // Soul absorption: resonant inhale with reverb tail
        const now = ctx.currentTime;

        // Low resonant tone (soul being drawn in)
        const osc1 = ctx.createOscillator();
        const gain1 = ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(220, now);
        osc1.frequency.exponentialRampToValueAtTime(440, now + 0.15);
        osc1.frequency.exponentialRampToValueAtTime(660, now + 0.3);
        gain1.gain.setValueAtTime(0.15 * masterVol, now);
        gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc1.connect(gain1);
        gain1.connect(ctx.destination);
        osc1.start(now);
        osc1.stop(now + 0.5);

        // High shimmer (soul sparkle)
        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(1320, now + 0.05);
        osc2.frequency.exponentialRampToValueAtTime(1760, now + 0.2);
        gain2.gain.setValueAtTime(0.08 * masterVol, now + 0.05);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
        osc2.connect(gain2);
        gain2.connect(ctx.destination);
        osc2.start(now + 0.05);
        osc2.stop(now + 0.45);
    },

    combo: (ctx, masterVol) => {
        // Crystal resonance cascade - minor scale cave echoes
        const now = ctx.currentTime;
        // D minor pentatonic: D5, F5, G5, A5
        const freqs = [587.33, 698.46, 783.99, 880];

        freqs.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + i * 0.1);

            gain.gain.setValueAtTime(0.1 * masterVol, now + i * 0.1);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.6);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.1);
            osc.stop(now + i * 0.1 + 0.6);

            // Sub-harmonic echo
            const sub = ctx.createOscillator();
            const subGain = ctx.createGain();
            sub.type = 'sine';
            sub.frequency.setValueAtTime(freq * 0.5, now + i * 0.1 + 0.2);
            subGain.gain.setValueAtTime(0.03 * masterVol, now + i * 0.1 + 0.2);
            subGain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.8);
            sub.connect(subGain);
            subGain.connect(ctx.destination);
            sub.start(now + i * 0.1 + 0.2);
            sub.stop(now + i * 0.1 + 0.8);
        });
    },

    fever: (ctx, masterVol) => {
        // Void burst: deep rumble with ascending soul energy
        const now = ctx.currentTime;

        // Deep rumble base
        const bass = ctx.createOscillator();
        const bassGain = ctx.createGain();
        bass.type = 'sawtooth';
        bass.frequency.setValueAtTime(55, now);
        bass.frequency.linearRampToValueAtTime(110, now + 0.5);

        const bassFilter = ctx.createBiquadFilter();
        bassFilter.type = 'lowpass';
        bassFilter.frequency.setValueAtTime(200, now);
        bassFilter.frequency.linearRampToValueAtTime(400, now + 0.5);

        bassGain.gain.setValueAtTime(0.001, now);
        bassGain.gain.linearRampToValueAtTime(0.15 * masterVol, now + 0.3);
        bassGain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);

        bass.connect(bassFilter);
        bassFilter.connect(bassGain);
        bassGain.connect(ctx.destination);
        bass.start(now);
        bass.stop(now + 1.5);

        // Soul energy chord: Dm voicing
        const chordFreqs = [146.83, 220, 293.66, 440];
        chordFreqs.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + 0.2);

            const lfo = ctx.createOscillator();
            const lfoGain = ctx.createGain();
            lfo.frequency.setValueAtTime(4 + i, now);
            lfoGain.gain.setValueAtTime(2, now);
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            lfo.start(now + 0.2);
            lfo.stop(now + 1.8);

            gain.gain.setValueAtTime(0.001, now + 0.2);
            gain.gain.linearRampToValueAtTime(0.08 * masterVol, now + 0.5);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 1.8);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + 0.2);
            osc.stop(now + 1.8);
        });
    },

    gameover: (ctx, masterVol) => {
        // Mask cracking: sharp attack + hollow decay
        const now = ctx.currentTime;

        // Crack sound (noise burst)
        const crack = ctx.createOscillator();
        const crackFilter = ctx.createBiquadFilter();
        const crackGain = ctx.createGain();
        crack.type = 'sawtooth';
        crack.frequency.setValueAtTime(150, now);
        crack.frequency.linearRampToValueAtTime(50, now + 0.3);
        crackFilter.type = 'lowpass';
        crackFilter.frequency.setValueAtTime(800, now);
        crackFilter.frequency.exponentialRampToValueAtTime(100, now + 0.5);
        crackGain.gain.setValueAtTime(0.2 * masterVol, now);
        crackGain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        crack.connect(crackFilter);
        crackFilter.connect(crackGain);
        crackGain.connect(ctx.destination);
        crack.start(now);
        crack.stop(now + 0.3);

        // Hollow descent (minor seconds falling)
        const notes = [
            { freq: 293.66, start: 0.2, dur: 1.0 },
            { freq: 277.18, start: 0.4, dur: 1.0 },
            { freq: 220, start: 0.6, dur: 1.2 },
            { freq: 146.83, start: 0.9, dur: 1.5 }
        ];

        notes.forEach(note => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(note.freq, now + note.start);
            osc.frequency.linearRampToValueAtTime(note.freq * 0.92, now + note.start + note.dur);
            gain.gain.setValueAtTime(0.001, now + note.start);
            gain.gain.linearRampToValueAtTime(0.1 * masterVol, now + note.start + 0.1);
            gain.gain.exponentialRampToValueAtTime(0.001, now + note.start + note.dur);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + note.start);
            osc.stop(now + note.start + note.dur + 0.1);
        });
    },

    levelup: (ctx, masterVol) => {
        // Bench save: warm melody with gentle reverb feel
        const now = ctx.currentTime;
        // D major pentatonic ascending: D5, E5, F#5, A5, B5, D6
        const freqs = [587.33, 659.25, 739.99, 880, 987.77, 1174.66];

        freqs.forEach((f, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(f, now + i * 0.12);
            gain.gain.setValueAtTime(0.12 * masterVol, now + i * 0.12);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.7);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.12);
            osc.stop(now + i * 0.12 + 0.7);

            // Warm sub octave
            const sub = ctx.createOscillator();
            const subGain = ctx.createGain();
            sub.type = 'sine';
            sub.frequency.setValueAtTime(f * 0.5, now + i * 0.12);
            subGain.gain.setValueAtTime(0.04 * masterVol, now + i * 0.12);
            subGain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.5);
            sub.connect(subGain);
            subGain.connect(ctx.destination);
            sub.start(now + i * 0.12);
            sub.stop(now + i * 0.12 + 0.5);
        });
    }
};
