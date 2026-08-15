function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}

function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 120;
    if (window.scrollY >= sectionTop) {
      current = section.id;
    }
  });
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === '#' + current);
  });
}

const BUSINESS_EMAIL = 'guinnoukoami@gmail.com';
const BUSINESS_WHATSAPP = '22892888759';

function toggleScrollTop() {
  const btn = document.getElementById('scrollTop');
  if (btn) btn.classList.toggle('show', window.scrollY > 400);
}

function showSuccessMessage(selector) {
  const success = document.getElementById(selector);
  if (success) {
    success.style.display = 'block';
    setTimeout(() => { success.style.display = 'none'; }, 5000);
  }
}

function openMail(subject, body) {
  const mailto = `mailto:${BUSINESS_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  window.open(mailto, '_blank');
}

function openWhatsApp(message) {
  const text = encodeURIComponent(message);
  const wa = `https://wa.me/${BUSINESS_WHATSAPP}?text=${text}`;
  window.open(wa, '_blank', 'noopener,noreferrer');
}

function openWhatsAppForProduct(button) {
  const productName = button.dataset.product || 'Produit';
  const category = button.dataset.category || 'Produit';
  const message = `Bonjour Ro Business Center, je souhaite commander ${productName}. Catégorie : ${category}. Merci de me recontacter.`;
  openWhatsApp(message);
}

async function submitInscription(event) {
  event.preventDefault();
  const prenom = document.getElementById('prenom').value.trim();
  const nom = document.getElementById('nom').value.trim();
  const tel = document.getElementById('tel').value.trim();
  const email = document.getElementById('email').value.trim();
  const formation = document.getElementById('formation').value;
  const message = document.getElementById('inscMessage').value.trim();
  if (!prenom || !tel || !formation) {
    alert('Veuillez remplir les champs obligatoires : Prénom, Téléphone et Formation.');
    return;
  }
  try {
    await fetch('/inscription', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prenom, nom, tel, email, formation, message })
    });
  } catch (error) {
    console.warn('Backend indisponible, la soumission est simulée.', error);
  }
  showSuccessMessage('inscSuccess');
  document.getElementById('inscriptionForm').reset();
}

async function submitContact(event) {
  event.preventDefault();
  const nom = document.getElementById('cNom').value.trim();
  const contact = document.getElementById('cContact').value.trim();
  const sujet = document.getElementById('cSujet').value;
  const message = document.getElementById('cMessage').value.trim();
  if (!nom || !message) {
    alert('Veuillez remplir votre nom et votre message.');
    return;
  }
  try {
    await fetch('/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: nom, contact: contact, subject: sujet, message: message })
    });
  } catch (error) {
    console.warn('Backend indisponible, la soumission est simulée.', error);
  }
  showSuccessMessage('contactSuccess');
  document.getElementById('contactForm').reset();
}

document.addEventListener('DOMContentLoaded', () => {
  updateActiveNav();
  document.getElementById('inscriptionForm')?.addEventListener('submit', submitInscription);
  document.getElementById('contactForm')?.addEventListener('submit', submitContact);
  document.querySelectorAll('.mobile-menu a').forEach(link => link.addEventListener('click', toggleMenu));
  document.getElementById('scrollTop')?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  document.querySelectorAll('[data-whatsapp-product="true"]').forEach(btn => {
    btn.addEventListener('click', () => openWhatsAppForProduct(btn));
  });
  // Setup boutique search if present
  const boutiqueSearch = document.getElementById('boutiqueSearch');
  if (boutiqueSearch) {
    let timer = null;
    boutiqueSearch.addEventListener('input', (e) => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        const q = (e.target.value || '').toLowerCase().trim();
        document.querySelectorAll('.product-card').forEach(card => {
          const name = (card.dataset.name || '').toLowerCase();
          const desc = (card.dataset.desc || '').toLowerCase();
          const ok = q === '' || name.includes(q) || desc.includes(q);
          card.style.display = ok ? '' : 'none';
        });
      }, 180);
    });
  }
});

window.addEventListener('scroll', () => {
  updateActiveNav();
  toggleScrollTop();
});
