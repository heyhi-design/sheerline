---
name: framer-motion-patterns
zone: 2
load_trigger: Build requires React animation — exit animations, layout transitions, gesture-driven motion, or coordinated component sequences
token_estimate: ~900
classification: HeyHi Internal Use Only
created: 2026-04-18
version: "1.0.0"
---

# Framer Motion Patterns

Reference for React animation work using Framer Motion (rebranded as `motion` in late 2024). Load when a build requires exit animations, layout animations, gesture-driven motion, or complex choreography that CSS scroll-driven animations cannot handle.

The companion file `interaction-patterns.md` covers CSS-native scroll-driven animations and View Transitions — load that for zero-JS motion on marketing pages. Load this file when you need React component lifecycle animation, drag/swipe gestures, or shared layout transitions.

---

## Import Path

**Import path changed in late 2024:** `import { motion, AnimatePresence } from 'motion/react'`

The old `framer-motion` package still works but `motion/react` is the forward-compatible path. Always use the new import in new code.

---

## The Four Core Primitives

```jsx
// 1. motion component — any HTML element becomes animatable
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.4, ease: [0.33, 1, 0.68, 1] }}
/>

// 2. variants — named states, propagate to children automatically
const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08 }
  })
};

// 3. AnimatePresence — enables exit animations for unmounted components
// The component MUST be inside AnimatePresence for exit to fire
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="panel"
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      exit="hidden"
    />
  )}
</AnimatePresence>

// 4. Gestures
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
/>
```

---

## AnimatePresence — Mode and Custom Props

For content swaps where the outgoing element should finish before the incoming one mounts:

```jsx
import { AnimatePresence, motion } from 'motion/react';

// mode="wait" — outgoing animation completes before incoming starts
// custom prop — passes current value to variants for direction-aware animation
<AnimatePresence mode="wait" custom={direction}>
  <motion.div
    key={currentPage}
    custom={direction}
    variants={{
      enter: (dir) => ({ x: dir > 0 ? 300 : -300, opacity: 0 }),
      center: { x: 0, opacity: 1 },
      exit:  (dir) => ({ x: dir > 0 ? -300 : 300, opacity: 0 }),
    }}
    initial="enter"
    animate="center"
    exit="exit"
    transition={{ duration: 0.3 }}
  >
    {content}
  </motion.div>
</AnimatePresence>
```

Key rules:
- Keying the animated component is required — `key` tells AnimatePresence when an element has been replaced.
- `mode="wait"` prevents overlap during transitions; omit it when overlap is intentional.
- `custom` passes external data into variant functions without re-declaring the variant.

---

## Scroll Animations

```jsx
import { useScroll, useTransform, motion } from 'motion/react';

// Parallax tied to page scroll
function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -100]);
  return <motion.div style={{ y }} />;
}

// Viewport-triggered reveal — replaces IntersectionObserver for simple cases
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-60px" }}
/>
```

`once: true` fires the animation only on the first entry — correct for editorial reveals. Omit it for elements that should re-animate on each scroll-into-view.

---

## Layout Animations

```jsx
// Automatically animates between layout positions using FLIP internally
<motion.div layout>
  {/* Any CSS change to size or position animates smoothly */}
</motion.div>

// Shared layout — element appears to move between two different components
// Both components must share the same layoutId
<motion.div layoutId="hero-image" />
```

Layout animations are the capability most difficult to replicate with CSS alone. Use when elements reflow into new positions (expanded accordions, grid resorting, card expand-to-detail).

---

## Gesture-Driven Motion: useMotionValue + useSpring + useTransform

This pattern is the correct tool for drag, swipe, and pull-to-refresh interfaces. `useMotionValue` does not trigger React re-renders on change — critical for 60fps gesture tracking.

```jsx
import { useMotionValue, useSpring, useTransform, motion } from 'motion/react';

// Drag-to-dismiss card — common in financial UI
function DismissibleCard({ onDismiss, children }) {
  const x = useMotionValue(0);
  // useSpring adds inertia — makes drag feel physical
  const springX = useSpring(x, { stiffness: 300, damping: 30 });
  const opacity = useTransform(x, [-150, 0, 150], [0, 1, 0]);

  function handleDragEnd(_, info) {
    if (Math.abs(info.offset.x) > 100) onDismiss();
  }

  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      style={{ x: springX, opacity }}
      onDragEnd={handleDragEnd}
    >
      {children}
    </motion.div>
  );
}
```

| Hook | What it does |
|------|-------------|
| `useMotionValue(0)` | Creates a value that updates without React re-render |
| `useSpring(value, config)` | Wraps any motion value in spring physics |
| `useTransform(value, input, output)` | Maps one range to another (x position → opacity) |

---

## Choreography at Scale — Stagger and Sequence

**Stagger via variants:**

```jsx
const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={item} />
  ))}
</motion.ul>
```

**Sequence control** — for brand intro sequences or loading sequences where timing must be exact:

```javascript
import { animate } from 'motion';

// Fine-grained sequencing without React state
animate([
  ['.logo',    { opacity: [0, 1] },                   { duration: 0.4 }],
  ['.tagline', { y: [20, 0], opacity: [0, 1] },       { at: '-0.2' }],
  ['.cta',     { opacity: [0, 1] },                   { at: '+0.1' }]
]);
```

`at: '-0.2'` starts the tagline 0.2 seconds before the logo finishes (overlap). `at: '+0.1'` starts the CTA 0.1 seconds after the tagline starts.

---

## Reduced Motion

Always implement reduced motion support. Two approaches:

```jsx
import { MotionConfig } from 'motion/react';

// App-level — respects system preference automatically
<MotionConfig reducedMotion="user">
  {children}
</MotionConfig>

// Per-component
import { useReducedMotion } from 'motion/react';

function AnimatedCard() {
  const shouldReduce = useReducedMotion();
  return (
    <motion.div
      animate={{ opacity: 1, y: shouldReduce ? 0 : [20, 0] }}
    />
  );
}
```

`MotionConfig reducedMotion="user"` is the preferred approach — wrap the app once, all motion respects the preference without per-component handling.

---

## Performance Rules

- Animate `transform` and `opacity` only — compositor thread, no layout recalculation.
- Add `willChange: "transform"` only on elements that actually animate — do not apply globally.
- Exit animations require the component to be inside `<AnimatePresence>` — if exit isn't firing, check this first.
- For 60fps gesture tracking, use `useMotionValue` — do not use React state to track drag position.

---

## Decision Matrix

| Need | Solution |
|------|---------|
| Scroll-linked reveal on a marketing page | `whileInView` prop |
| Content swap / tab change | View Transitions API (see `interaction-patterns.md`) |
| Component mount/unmount with exit animation | `AnimatePresence` + `motion.*` |
| Element moves position in the layout | `motion.div layout` |
| Parallax effect | `useScroll` + `useTransform` |
| Gesture-driven (drag, swipe, pull-to-refresh) | `useMotionValue` + `useSpring` + `useTransform` |
| Pure CSS visual effect on scroll | CSS scroll-driven (see `interaction-patterns.md`) |
| Multi-element entrance sequence | variants + `staggerChildren` |
| Brand intro / loading sequence | `animate()` function from `motion` |

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Load when build requires React component lifecycle animation or gesture-driven motion. v1.0.0 created 2026-04-18 from frontend-research-reference.md v1.2.0.*
