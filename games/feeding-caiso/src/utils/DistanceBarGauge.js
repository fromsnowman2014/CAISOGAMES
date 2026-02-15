import { GAME_CONFIG } from './Constants.js';

/**
 * DistanceBarGauge - Timing-based power meter for feeding mechanic
 * Design A: Horizontal bar showing power level with color-coded zones
 *
 * Visual Design:
 * - 260px x 20px horizontal bar at bottom center
 * - Needle oscillates left-right (0→1→0 with bounce)
 * - 5 color zones: Red (miss) → Yellow (good) → Green (perfect) → Yellow → Red
 * - Diamond-shaped needle with Soul Blue glow
 *
 * Mechanics:
 * - Needle speed scales with stage difficulty (1.0x to 2.5x)
 * - Perfect zone: 40-60% (20% width, green)
 * - Good zones: 25-40% and 60-75% (15% each, yellow)
 * - Miss zones: 0-25% and 75-100% (25% each, red)
 *
 * Integration:
 * - checkTiming() returns {result, power, color} for throw calculation
 * - power value (0-1) maps to throw distance multiplier in Food.js
 */
export class DistanceBarGauge {
    constructor() {
        // Position (centered at bottom, above combo counter)
        this.x = GAME_CONFIG.WIDTH / 2;
        this.y = GAME_CONFIG.HEIGHT - 110;
        this.width = 260;
        this.height = 20;

        // Needle state
        this.needlePosition = 0.5;  // Normalized 0-1 (0=left, 1=right)
        this.direction = 1;         // 1=moving right, -1=moving left
        this.baseSpeed = 0.0015;    // Speed per millisecond
        this.speedMultiplier = 1.0; // Stage difficulty multiplier

        // Zone definitions (normalized positions 0-1)
        // Left → Right: Too weak → Close → Perfect → Close → Too strong
        this.zones = {
            miss_left: {
                start: 0.00,
                end: 0.25,
                color: '#ff7675',      // Hollow Knight: Infection Red
                label: 'TOO WEAK'
            },
            good_left: {
                start: 0.25,
                end: 0.40,
                color: '#ffd93d',      // Hollow Knight: Lumafly Yellow
                label: 'GOOD'
            },
            perfect: {
                start: 0.40,
                end: 0.60,
                color: '#00b894',      // Hollow Knight: Moss Green
                label: 'PERFECT'
            },
            good_right: {
                start: 0.60,
                end: 0.75,
                color: '#ffd93d',      // Hollow Knight: Lumafly Yellow
                label: 'GOOD'
            },
            miss_right: {
                start: 0.75,
                end: 1.00,
                color: '#ff7675',      // Hollow Knight: Infection Red
                label: 'TOO STRONG'
            }
        };

        // Feedback system
        this.feedbackTimer = 0;
        this.feedbackDuration = 300;  // 300ms flash (child-safe: <500ms)
        this.feedbackColor = null;
        this.feedbackText = '';

        // Tutorial state
        this.showTutorial = true;
        this.tutorialAlpha = 1.0;
    }

    /**
     * Update needle position with oscillation
     * Needle bounces at edges (0 and 1) for smooth back-and-forth motion
     */
    update(deltaTime) {
        // Move needle
        const speed = this.baseSpeed * this.speedMultiplier;
        this.needlePosition += speed * this.direction * deltaTime;

        // Bounce at edges
        if (this.needlePosition >= 1.0) {
            this.needlePosition = 1.0;
            this.direction = -1;  // Reverse to move left
        } else if (this.needlePosition <= 0.0) {
            this.needlePosition = 0.0;
            this.direction = 1;   // Reverse to move right
        }

        // Update feedback flash
        if (this.feedbackTimer > 0) {
            this.feedbackTimer -= deltaTime;
        }

        // Fade tutorial after first few throws
        if (this.showTutorial && this.tutorialAlpha > 0) {
            this.tutorialAlpha = Math.max(0, this.tutorialAlpha - deltaTime * 0.0003);
        }
    }

    /**
     * Check current timing when space bar is pressed
     * Returns timing result with power level for throw distance calculation
     *
     * @returns {{result: string, power: number, color: string, label: string}}
     */
    checkTiming() {
        const pos = this.needlePosition;

        // Check zones from center outward
        if (pos >= 0.40 && pos <= 0.60) {
            return {
                result: 'perfect',
                power: pos,
                color: this.zones.perfect.color,
                label: this.zones.perfect.label
            };
        } else if ((pos >= 0.25 && pos < 0.40) || (pos > 0.60 && pos <= 0.75)) {
            return {
                result: 'good',
                power: pos,
                color: pos < 0.5 ? this.zones.good_left.color : this.zones.good_right.color,
                label: 'GOOD'
            };
        } else {
            return {
                result: 'miss',
                power: pos,
                color: pos < 0.5 ? this.zones.miss_left.color : this.zones.miss_right.color,
                label: pos < 0.5 ? this.zones.miss_left.label : this.zones.miss_right.label
            };
        }
    }

    /**
     * Trigger visual feedback after timing check
     * Shows 300ms color flash and result text
     */
    triggerFeedback(timingResult) {
        this.feedbackTimer = this.feedbackDuration;
        this.feedbackColor = timingResult.color;
        this.feedbackText = timingResult.label;

        // Hide tutorial after first throw
        this.showTutorial = false;
    }

    /**
     * Set difficulty based on current stage
     * Needle moves faster in later stages
     *
     * Stage 1-2:  1.0x speed (easy)
     * Stage 3-4:  1.2x speed
     * Stage 5-7:  1.5x speed
     * Stage 8-9:  2.0x speed
     * Stage 10+:  2.5x speed (very fast)
     */
    setDifficulty(stageIndex) {
        const speedMap = {
            0: 1.0,   // Stage 1-2
            1: 1.0,
            2: 1.2,   // Stage 3-4
            3: 1.2,
            4: 1.5,   // Stage 5-7
            5: 1.5,
            6: 1.5,
            7: 2.0,   // Stage 8-9
            8: 2.0,
            9: 2.5    // Stage 10+
        };

        this.speedMultiplier = speedMap[stageIndex] || 2.5;
    }

    /**
     * Draw the distance bar gauge with all visual elements
     * - Background bar with 5 colored zones
     * - Oscillating diamond needle with glow
     * - Feedback flash on successful/failed timing
     * - "POWER" label
     * - Tutorial hint (first 3 throws)
     */
    draw(ctx) {
        ctx.save();

        // Calculate bar bounds
        const barX = this.x - this.width / 2;
        const barY = this.y - this.height / 2;

        // Draw background container
        ctx.fillStyle = 'rgba(15, 15, 27, 0.8)';  // Hollow Knight: Void Black
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(barX - 4, barY - 4, this.width + 8, this.height + 8, 6);
        } else {
            ctx.rect(barX - 4, barY - 4, this.width + 8, this.height + 8);
        }
        ctx.fill();

        // Draw 5 colored zones
        Object.values(this.zones).forEach(zone => {
            const zoneX = barX + zone.start * this.width;
            const zoneWidth = (zone.end - zone.start) * this.width;

            ctx.fillStyle = zone.color;
            ctx.globalAlpha = 0.3;  // Subtle background color
            ctx.fillRect(zoneX, barY, zoneWidth, this.height);
        });
        ctx.globalAlpha = 1.0;

        // Draw zone borders for clarity
        ctx.strokeStyle = 'rgba(178, 190, 195, 0.2)';
        ctx.lineWidth = 1;
        [0.25, 0.40, 0.60, 0.75].forEach(pos => {
            const lineX = barX + pos * this.width;
            ctx.beginPath();
            ctx.moveTo(lineX, barY);
            ctx.lineTo(lineX, barY + this.height);
            ctx.stroke();
        });

        // Draw feedback flash overlay
        if (this.feedbackTimer > 0 && this.feedbackColor) {
            const flashAlpha = this.feedbackTimer / this.feedbackDuration;
            ctx.fillStyle = this.feedbackColor;
            ctx.globalAlpha = flashAlpha * 0.4;
            ctx.beginPath();
            if (ctx.roundRect) {
                ctx.roundRect(barX, barY, this.width, this.height, 4);
            } else {
                ctx.rect(barX, barY, this.width, this.height);
            }
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }

        // Draw diamond-shaped needle with Soul Blue glow
        const needleX = barX + this.needlePosition * this.width;
        const needleY = barY + this.height / 2;

        // Glow effect
        ctx.shadowColor = '#74b9ff';  // Soul Blue
        ctx.shadowBlur = 12;
        ctx.fillStyle = '#74b9ff';
        ctx.beginPath();
        ctx.moveTo(needleX, needleY - 14);           // Top point
        ctx.lineTo(needleX + 6, needleY);            // Right point
        ctx.lineTo(needleX, needleY + 14);           // Bottom point
        ctx.lineTo(needleX - 6, needleY);            // Left point
        ctx.closePath();
        ctx.fill();

        // Inner diamond (brighter)
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#dfe6e9';  // Pale White
        ctx.beginPath();
        ctx.moveTo(needleX, needleY - 10);
        ctx.lineTo(needleX + 4, needleY);
        ctx.lineTo(needleX, needleY + 10);
        ctx.lineTo(needleX - 4, needleY);
        ctx.closePath();
        ctx.fill();

        // Draw border around entire bar
        ctx.strokeStyle = '#b2bec3';  // Grayish border
        ctx.lineWidth = 2;
        ctx.shadowBlur = 0;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(barX - 4, barY - 4, this.width + 8, this.height + 8, 6);
        } else {
            ctx.rect(barX - 4, barY - 4, this.width + 8, this.height + 8);
        }
        ctx.stroke();

        // Draw "POWER" label above bar
        ctx.fillStyle = '#dfe6e9';
        ctx.font = 'bold 12px Fredoka One';
        ctx.textAlign = 'center';
        ctx.fillText('POWER', this.x, barY - 12);

        // Draw tutorial hint (first 3 throws)
        if (this.showTutorial && this.tutorialAlpha > 0) {
            ctx.globalAlpha = this.tutorialAlpha;
            ctx.fillStyle = '#ffd93d';
            ctx.font = '11px Nunito';
            ctx.fillText('Press SPACE when needle is in GREEN zone!', this.x, barY - 28);
            ctx.globalAlpha = 1.0;
        }

        // Draw feedback text below bar
        if (this.feedbackTimer > 0 && this.feedbackText) {
            const textAlpha = this.feedbackTimer / this.feedbackDuration;
            ctx.globalAlpha = textAlpha;
            ctx.fillStyle = this.feedbackColor;
            ctx.font = 'bold 14px Fredoka One';
            ctx.fillText(this.feedbackText, this.x, barY + this.height + 22);
            ctx.globalAlpha = 1.0;
        }

        ctx.restore();
    }

    /**
     * Reset gauge state (called when game restarts)
     */
    reset() {
        this.needlePosition = 0.5;
        this.direction = 1;
        this.speedMultiplier = 1.0;
        this.feedbackTimer = 0;
        this.feedbackColor = null;
        this.feedbackText = '';
        this.showTutorial = true;
        this.tutorialAlpha = 1.0;
    }
}
