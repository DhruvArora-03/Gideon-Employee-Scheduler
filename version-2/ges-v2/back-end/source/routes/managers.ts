import express from 'express';
import controller from '../controllers/managers';

const router = express.Router();

router.get('/managers', controller.getManagers);
router.post('/managers', controller.addManager);

router.get('/manager/:id', controller.getManager);
router.put('/manager/:id', controller.updateManager);
router.delete('/manager/:id', controller.deleteManager);

export default router;