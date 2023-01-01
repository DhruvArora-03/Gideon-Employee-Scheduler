import express from 'express';
import controller from '../controllers/availability';

const router = express.Router();

router.get('/employee/availbility/:id', controller.getAvailability);
router.put('/employee/availbility/:id', controller.updateAvailability);

export default router;