import { GAME_CONFIG } from '../utils/Constants.js';

export class VirtualJoystick {
    constructor(canvas) {
        this.canvas = canvas;
        this.active = false;
        this.origin = { x: 0, y: 0 };
        this.current = { x: 0, y: 0 };
        this.direction = { x: 0, y: 0 };
        this.radius = 60;

        this.setupListeners();
    }

    setupListeners() {
        // Touch events
        this.canvas.addEventListener('touchstart', (e) => this.handleStart(e), { passive: false });
        this.canvas.addEventListener('touchmove', (e) => this.handleMove(e), { passive: false });
        this.canvas.addEventListener('touchend', () => this.handleEnd());

        // Mouse events (for testing)
        this.canvas.addEventListener('mousedown', (e) => this.handleStart(e));
        window.addEventListener('mousemove', (e) => this.handleMove(e));
        window.addEventListener('mouseup', () => this.handleEnd());
    }

    getPos(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;

        let clientX, clientY;
        if (e.touches && e.touches.length > 0) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        } else {
            clientX = e.clientX;
            clientY = e.clientY;
        }

        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY
        };
    }

    handleStart(e) {
        // Ignore clicks on UI elements (simple zone check)
        const pos = this.getPos(e);
        if (pos.y < GAME_CONFIG.HEIGHT - GAME_CONFIG.CONTROL_HEIGHT) return;

        // Prevent default only if in control zone
        e.preventDefault();

        this.active = true;
        this.origin = pos;
        this.current = pos;
        this.updateDirection();
    }

    handleMove(e) {
        if (!this.active) return;
        e.preventDefault();

        this.current = this.getPos(e);

        // Clamp current position to radius
        const dx = this.current.x - this.origin.x;
        const dy = this.current.y - this.origin.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > this.radius) {
            const angle = Math.atan2(dy, dx);
            this.current.x = this.origin.x + Math.cos(angle) * this.radius;
            this.current.y = this.origin.y + Math.sin(angle) * this.radius;
        }

        this.updateDirection();
    }

    handleEnd() {
        this.active = false;
        this.direction = { x: 0, y: 0 };
    }

    updateDirection() {
        const dx = this.current.x - this.origin.x;
        const dy = this.current.y - this.origin.y;

        // Normalize
        const maxDist = this.radius;
        this.direction = {
            x: dx / maxDist,
            y: dy / maxDist
        };
    }

    draw(ctx) {
        if (!this.active) return;

        ctx.save();

        // Base
        ctx.beginPath();
        ctx.arc(this.origin.x, this.origin.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();

        // Knob
        ctx.beginPath();
        ctx.arc(this.current.x, this.current.y, 25, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.fill();

        ctx.restore();
    }
}
