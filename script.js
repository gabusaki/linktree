gsap.from(".profile", { 
    duration: 1.2, 
    y: -50, 
    opacity: 0, 
    ease: "power3.out"
});

    gsap.from(".link-card", {
        opacity:0,
        y:30
    },
    {
    duration: 0.8, 
    y: 30, 
    opacity: 1,
    stagger: 0.2, 
    delay: 0.4, 
    ease: "back.out(1.7)"
});